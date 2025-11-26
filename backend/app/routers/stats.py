from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Question, Company, Topic

router = APIRouter()

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """
    Get overall statistics about the question database.
    """
    # Total questions
    total_questions = db.query(func.count(Question.id)).scalar()
    
    # Questions by category
    by_category = db.query(
        Question.category,
        func.count(Question.id)
    ).group_by(Question.category).all()
    
    # Questions by difficulty
    by_difficulty = db.query(
        Question.difficulty,
        func.count(Question.id)
    ).group_by(Question.difficulty).all()
    
    # Total companies
    total_companies = db.query(func.count(Company.id)).scalar()
    
    # Total topics
    total_topics = db.query(func.count(Topic.id)).scalar()
    
    # Top 5 companies by question count
    top_companies = db.query(
        Company.name,
        func.count(Question.id).label('count')
    ).join(Company.questions)\
     .group_by(Company.name)\
     .order_by(func.count(Question.id).desc())\
     .limit(5)\
     .all()
    
    # Top 5 topics by question count
    top_topics = db.query(
        Topic.name,
        func.count(Question.id).label('count')
    ).join(Topic.questions)\
     .group_by(Topic.name)\
     .order_by(func.count(Question.id).desc())\
     .limit(5)\
     .all()
    
    return {
        "total_questions": total_questions,
        "total_companies": total_companies,
        "total_topics": total_topics,
        "by_category": {cat: count for cat, count in by_category},
        "by_difficulty": {diff: count for diff, count in by_difficulty},
        "top_companies": [{"name": name, "count": count} for name, count in top_companies],
        "top_topics": [{"name": name, "count": count} for name, count in top_topics]
    }


@router.get("/stats/category/{category}")
def get_category_stats(category: str, db: Session = Depends(get_db)):
    """
    Get detailed statistics for a specific category.
    """
    # Total questions in category
    total = db.query(func.count(Question.id))\
        .filter(Question.category == category)\
        .scalar()
    
    # By difficulty
    by_difficulty = db.query(
        Question.difficulty,
        func.count(Question.id)
    ).filter(Question.category == category)\
     .group_by(Question.difficulty)\
     .all()
    
    # Top companies for this category
    top_companies = db.query(
        Company.name,
        func.count(Question.id).label('count')
    ).join(Company.questions)\
     .filter(Question.category == category)\
     .group_by(Company.name)\
     .order_by(func.count(Question.id).desc())\
     .limit(10)\
     .all()
    
    # Top topics for this category
    top_topics = db.query(
        Topic.name,
        func.count(Question.id).label('count')
    ).join(Topic.questions)\
     .filter(Question.category == category)\
     .group_by(Topic.name)\
     .order_by(func.count(Question.id).desc())\
     .limit(10)\
     .all()
    
    return {
        "category": category,
        "total_questions": total,
        "by_difficulty": {diff: count for diff, count in by_difficulty},
        "top_companies": [{"name": name, "count": count} for name, count in top_companies],
        "top_topics": [{"name": name, "count": count} for name, count in top_topics]
    }