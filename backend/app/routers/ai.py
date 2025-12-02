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

    # Step 1: Retrieval - Search for relevant questions in the database
    search_terms = request.query.lower()

    # Search in title, content, category
    questions_query = db.query(Question).filter(
        or_(
            Question.title.ilike(f"%{search_terms}%"),
            Question.content.ilike(f"%{search_terms}%"),
            Question.category.ilike(f"%{search_terms}%")
        )
    ).limit(5).all()

    # If no questions found with full query, try to extract key terms
    if not questions_query:
        # Try searching with individual words (simple keyword extraction)
        words = [w for w in search_terms.split() if len(w) > 3]
        if words:
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
