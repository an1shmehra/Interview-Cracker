from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Question, Company, Topic
from app.schemas.question import Question as QuestionSchema, QuestionList
from sqlalchemy import or_, func

router = APIRouter()

@router.get("/questions", response_model=QuestionList)
def get_questions(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    company: Optional[str] = None,
    topic: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = Query(20, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Get questions with optional filters and pagination.
    
    - **category**: Filter by category (DSA, System Design, Behavioral)
    - **difficulty**: Filter by difficulty (Easy, Medium, Hard)
    - **company**: Filter by company name
    - **topic**: Filter by topic slug
    - **search**: Search in title and content
    - **limit**: Number of results (max 100)
    - **offset**: Pagination offset
    """
    # Start with base query
    query = db.query(Question)
    
    # Apply filters
    if category:
        query = query.filter(Question.category == category)
    
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    
    if company:
        query = query.join(Question.companies).filter(Company.name.ilike(f"%{company}%"))
    
    if topic:
        query = query.join(Question.topics).filter(Topic.slug == topic)
    
    if search:
        search_filter = or_(
            Question.title.ilike(f"%{search}%"),
            Question.content.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    questions = query.offset(offset).limit(limit).all()
    
    return {
        "total": total,
        "questions": questions
    }


@router.get("/questions/{question_id}", response_model=QuestionSchema)
def get_question(question_id: int, db: Session = Depends(get_db)):
    """
    Get a single question by ID with all details (companies, topics).
    """
    question = db.query(Question).filter(Question.id == question_id).first()
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    return question


@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """
    Get all unique categories with question counts.
    """
    categories = db.query(
        Question.category,
        func.count(Question.id).label('count')
    ).group_by(Question.category).all()
    
    return {
        "categories": [
            {"name": cat, "count": count} 
            for cat, count in categories
        ]
    }


@router.get("/companies")
def get_companies(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """
    Get all companies with question counts.
    """
    companies = db.query(
        Company.name,
        func.count(Question.id).label('count')
    ).join(Company.questions)\
     .group_by(Company.name)\
     .order_by(func.count(Question.id).desc())\
     .limit(limit)\
     .all()
    
    return {
        "companies": [
            {"name": name, "count": count}
            for name, count in companies
        ]
    }


@router.get("/topics")
def get_topics(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """
    Get all topics with question counts.
    """
    topics = db.query(
        Topic.name,
        Topic.slug,
        func.count(Question.id).label('count')
    ).join(Topic.questions)\
     .group_by(Topic.name, Topic.slug)\
     .order_by(func.count(Question.id).desc())\
     .limit(limit)\
     .all()
    
    return {
        "topics": [
            {"name": name, "slug": slug, "count": count}
            for name, slug, count in topics
        ]
    }


@router.get("/difficulties")
def get_difficulties(db: Session = Depends(get_db)):
    """
    Get all difficulties with question counts.
    """
    difficulties = db.query(
        Question.difficulty,
        func.count(Question.id).label('count')
    ).group_by(Question.difficulty)\
     .order_by(func.count(Question.id).desc())\
     .all()
    
    return {
        "difficulties": [
            {"name": diff, "count": count}
            for diff, count in difficulties
        ]
    }