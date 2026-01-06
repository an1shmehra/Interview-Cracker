from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict
from app.database import get_db
from app.models import Question
from sqlalchemy import or_
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

router = APIRouter()

class QuestionProgress(BaseModel):
    question_id: int
    category: str
    difficulty: str
    status: Optional[str] = None  # 'completed', 'in_progress', or None

class AIRequest(BaseModel):
    query: str
    user_progress: Optional[List[QuestionProgress]] = None

class RecommendedQuestion(BaseModel):
    id: int
    title: str
    category: str
    difficulty: str

class DifficultyRecommendation(BaseModel):
    category: str
    recommended_difficulty: str
    reason: str
    completed_easy: int
    completed_medium: int
    completed_hard: int

class AIResponse(BaseModel):
    response: str
    recommended_questions: List[RecommendedQuestion]
    personalized_recommendations: Optional[List[DifficultyRecommendation]] = None

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

def analyze_user_progress(user_progress: Optional[List[QuestionProgress]]) -> List[DifficultyRecommendation]:
    """
    Analyze user's completion history and recommend next difficulty level for each category.
    Uses rule-based ML approach to personalize learning path.
    """
    if not user_progress:
        return []

    # Group progress by category
    category_stats: Dict[str, Dict[str, int]] = {}

    for progress in user_progress:
        if progress.status != 'completed':
            continue

        category = progress.category
        difficulty = progress.difficulty

        if category not in category_stats:
            category_stats[category] = {'Easy': 0, 'Medium': 0, 'Hard': 0}

        if difficulty in ['Easy', 'Medium', 'Hard']:
            category_stats[category][difficulty] += 1

    # Generate recommendations for each category
    recommendations = []

    for category, stats in category_stats.items():
        easy_count = stats['Easy']
        medium_count = stats['Medium']
        hard_count = stats['Hard']

        # Rule-based difficulty prediction
        if hard_count >= 5:
            recommended = 'Hard'
            reason = f'You\'ve mastered {hard_count} Hard problems! Keep challenging yourself.'
        elif medium_count >= 10:
            recommended = 'Hard'
            reason = f'Great progress on Medium! ({medium_count} completed) Ready for Hard challenges.'
        elif medium_count >= 5:
            recommended = 'Medium'
            reason = f'Solid Medium progress ({medium_count} completed). Mix in some Hard problems too!'
        elif easy_count >= 15:
            recommended = 'Medium'
            reason = f'You\'ve mastered Easy level! ({easy_count} completed) Time to level up to Medium.'
        elif easy_count >= 8:
            recommended = 'Medium'
            reason = f'Good Easy foundation ({easy_count} completed). Start mixing in Medium problems.'
        elif easy_count >= 3:
            recommended = 'Easy'
            reason = f'Building momentum! ({easy_count} completed) Complete a few more Easy before Medium.'
        else:
            recommended = 'Easy'
            reason = 'Start with Easy problems to build a strong foundation.'

        recommendations.append(DifficultyRecommendation(
            category=category,
            recommended_difficulty=recommended,
            reason=reason,
            completed_easy=easy_count,
            completed_medium=medium_count,
            completed_hard=hard_count
        ))

    return recommendations

@router.post("/ai/ask", response_model=AIResponse)
def ask_ai(
    request: AIRequest,
    db: Session = Depends(get_db)
):
    """
    AI-powered interview preparation assistant with personalized difficulty recommendations.

    - **query**: User's question or topic they want help with
    - **user_progress**: Optional list of user's question completion history

    Returns AI-generated advice, relevant question recommendations, and personalized difficulty predictions.
    """
    try:
        print(f"\n[DEBUG] Received request")
        print(f"[DEBUG] Query: {request.query}")
        print(f"[DEBUG] User progress type: {type(request.user_progress)}")
        print(f"[DEBUG] User progress: {request.user_progress}")

        try:
            # Analyze user progress and generate personalized recommendations
            personalized_recs = analyze_user_progress(request.user_progress)
            print(f"[DEBUG] Personalized recs generated: {len(personalized_recs)} recommendations")
        except Exception as e:
            print(f"[ERROR] Progress analysis failed: {str(e)}")
            import traceback
            traceback.print_exc()
            personalized_recs = []

        # Search for relevant questions in database
        print("[DEBUG] Starting question search...")
        detected_category = detect_category(request.query)
        search_terms = request.query.lower()
        questions_query = []

        # Get list of completed question IDs to exclude them
        completed_ids = []
        if request.user_progress:
            completed_ids = [p.question_id for p in request.user_progress if p.status == 'completed']
        print(f"[DEBUG] Excluding {len(completed_ids)} completed questions")

        # Category-based retrieval
        if detected_category:
            query = db.query(Question).filter(Question.category == detected_category)
            if completed_ids:
                query = query.filter(~Question.id.in_(completed_ids))
            questions_query = query.limit(10).all()

        # Fallback to keyword search
        if not questions_query:
            query = db.query(Question).filter(
                or_(
                    Question.title.ilike(f"%{search_terms}%"),
                    Question.content.ilike(f"%{search_terms}%"),
                    Question.category.ilike(f"%{search_terms}%")
                )
            )
            if completed_ids:
                query = query.filter(~Question.id.in_(completed_ids))
            questions_query = query.limit(10).all()

        # Word-based search as last resort
        if not questions_query:
            words = [w for w in search_terms.split() if len(w) > 3]
            if words:
                filters = [
                    or_(
                        Question.title.ilike(f"%{word}%"),
                        Question.content.ilike(f"%{word}%"),
                        Question.category.ilike(f"%{word}%")
                    ) for word in words
                ]
                query = db.query(Question).filter(or_(*filters))
                if completed_ids:
                    query = query.filter(~Question.id.in_(completed_ids))
                questions_query = query.limit(10).all()

        print(f"[DEBUG] Found {len(questions_query)} questions")

        # Build context from retrieved questions
        context_parts = []
        if questions_query:
            context_parts.append("Related practice questions:")
            for q in questions_query:
                context_parts.append(f"- {q.title} ({q.category}, {q.difficulty})")

        # Add personalized recommendations to context
        if personalized_recs:
            context_parts.append("\nUser's personalized learning path:")
            for rec in personalized_recs:
                context_parts.append(
                    f"- {rec.category}: Recommend {rec.recommended_difficulty} "
                    f"(Completed: {rec.completed_easy} Easy, {rec.completed_medium} Medium, {rec.completed_hard} Hard)"
                )

        context = "\n".join(context_parts)
        print("[DEBUG] Built context, calling Groq API...")

        # Call Groq API
        try:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise HTTPException(status_code=500, detail="GROQ_API_KEY not found")

            client = Groq(api_key=api_key)

            system_prompt = f"""You are an expert interview preparation coach specializing in technical interviews for software engineering, data science, and ML roles.

Your role is to:
- Provide clear, actionable advice for interview preparation
- Explain concepts in a way that's easy to understand
- Suggest study strategies and approaches
- Help users understand what interviewers are looking for
- Be encouraging and supportive
- Naturally mention relevant practice questions when appropriate

Context from question database:
{context}"""

            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": request.query}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=1000,
            )

            ai_response = chat_completion.choices[0].message.content
            print("[DEBUG] Groq API call successful")

        except Exception as e:
            print(f"[ERROR] Groq API failed: {str(e)}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")

        # Format recommended questions
        print("[DEBUG] Formatting response...")
        recommended = [
            RecommendedQuestion(
                id=q.id,
                title=q.title,
                category=q.category,
                difficulty=q.difficulty
            )
            for q in questions_query
        ]

        print(f"[DEBUG] Returning response with {len(recommended)} questions and {len(personalized_recs) if personalized_recs else 0} recommendations")

        return AIResponse(
            response=ai_response,
            recommended_questions=recommended,
            personalized_recommendations=personalized_recs if personalized_recs else None
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"\n[FATAL ERROR] Unexpected error in ask_ai endpoint:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
