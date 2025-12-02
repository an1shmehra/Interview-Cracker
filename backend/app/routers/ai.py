from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.database import get_db
from app.models import Question
from sqlalchemy import or_
import os
import traceback
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

router = APIRouter()

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
print(f"[DEBUG] Groq API Key loaded: {api_key[:20] if api_key else 'None'}...")
groq_client = Groq(api_key=api_key)

class AIRequest(BaseModel):
    query: str

class RecommendedQuestion(BaseModel):
    id: int
    title: str
    category: str
    difficulty: str

class AIResponse(BaseModel):
    response: str
    recommended_questions: List[RecommendedQuestion]

def detect_category(query: str) -> Optional[str]:
    """
    Detect which category the user is asking about based on keywords.
    Returns 'DSA', 'System Design', 'Behavioral', or None.
    """
    query_lower = query.lower()

    # System Design keywords
    system_design_keywords = [
        'system design', 'scalability', 'distributed', 'architecture',
        'load balancing', 'microservices', 'database design', 'caching',
        'rate limiting', 'api design', 'design a system', 'design an app'
    ]

    # DSA keywords
    dsa_keywords = [
        'algorithm', 'data structure', 'dsa', 'leetcode', 'coding',
        'array', 'linked list', 'tree', 'graph', 'dynamic programming',
        'sorting', 'searching', 'recursion', 'hash', 'stack', 'queue'
    ]

    # Behavioral keywords
    behavioral_keywords = [
        'behavioral', 'tell me about', 'describe a time', 'leadership',
        'conflict', 'teamwork', 'challenge', 'failure', 'success story'
    ]

    # Check for matches
    if any(keyword in query_lower for keyword in system_design_keywords):
        return 'System Design'
    elif any(keyword in query_lower for keyword in behavioral_keywords):
        return 'Behavioral'
    elif any(keyword in query_lower for keyword in dsa_keywords):
        return 'DSA'

    return None

@router.post("/ai/ask", response_model=AIResponse)
def ask_ai(
    request: AIRequest,
    db: Session = Depends(get_db)
):
    """
    AI-powered interview preparation assistant using RAG.

    - **query**: User's question or topic they want help with

    Returns AI-generated advice along with relevant question recommendations.
    """

    # Step 1: Detect category from user query
    detected_category = detect_category(request.query)
    print(f"[DEBUG] Detected category: {detected_category}")

    # Step 2: Retrieval - Search for relevant questions in the database
    search_terms = request.query.lower()
    questions_query = []

    # If category detected, prioritize questions from that category
    if detected_category:
        print(f"[DEBUG] Filtering by category: {detected_category}")
        questions_query = db.query(Question).filter(
            Question.category == detected_category
        ).limit(5).all()
        print(f"[DEBUG] Found {len(questions_query)} questions in {detected_category} category")

    # If no category-specific results or no category detected, do general keyword search
    if not questions_query:
        print(f"[DEBUG] Falling back to general keyword search")
        questions_query = db.query(Question).filter(
            or_(
                Question.title.ilike(f"%{search_terms}%"),
                Question.content.ilike(f"%{search_terms}%"),
                Question.category.ilike(f"%{search_terms}%")
            )
        ).limit(5).all()

    # If still no questions found, try searching with individual words
    if not questions_query:
        words = [w for w in search_terms.split() if len(w) > 3]
        if words:
            print(f"[DEBUG] Trying word-based search with: {words}")
            filters = [
                or_(
                    Question.title.ilike(f"%{word}%"),
                    Question.content.ilike(f"%{word}%"),
                    Question.category.ilike(f"%{word}%")
                ) for word in words
            ]
            questions_query = db.query(Question).filter(or_(*filters)).limit(5).all()

    # Step 2: Augmentation - Build context from retrieved questions
    context_parts = []
    if questions_query:
        context_parts.append("Related practice questions:")
        for i, q in enumerate(questions_query, 1):
            context_parts.append(f"- {q.title} ({q.category}, {q.difficulty})")
        context_parts.append("")

    context = "\n".join(context_parts)

    # Step 3: Generation - Call Groq API with context + user query
    system_prompt = """You are an expert interview preparation coach specializing in technical interviews for software engineering, data science, and ML roles.

Your role is to:
- Provide clear, actionable advice for interview preparation
- Explain concepts in a way that's easy to understand
- Suggest study strategies and approaches
- Help users understand what interviewers are looking for
- Be encouraging and supportive
- If you have knowledge of relevant practice questions on this topic, you can mention them naturally as examples

IMPORTANT: Do NOT mention databases, contexts, or that information was "provided" to you. Act as if you have this knowledge naturally."""

    user_prompt = f"""{context}

{request.query}"""

    try:
        # Call Groq API
        print(f"[DEBUG] Calling Groq API with query: {request.query[:50]}...")
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.3-70b-versatile",  # Latest Llama model (3.1 was decommissioned)
            temperature=0.7,
            max_tokens=1000,
        )

        ai_response = chat_completion.choices[0].message.content
        print(f"[DEBUG] Groq API call successful")

    except Exception as e:
        print(f"[ERROR] Groq API call failed: {str(e)}")
        print(f"[ERROR] Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error calling Groq API: {str(e)}")

    # Format recommended questions for response
    recommended = [
        RecommendedQuestion(
            id=q.id,
            title=q.title,
            category=q.category,
            difficulty=q.difficulty
        )
        for q in questions_query
    ]

    return AIResponse(
        response=ai_response,
        recommended_questions=recommended
    )
