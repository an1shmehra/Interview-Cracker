import json
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Question, Company, Topic

def import_questions():
    # Load cleaned data
    print("Loading cleaned data...")
    with open('/Users/anishmehra/Documents/GitHub/Interview-Cracker/data/cleaned/all_questions.json', 'r', encoding='utf-8') as f:
        questions_data = json.load(f)
    
    print(f"Found {len(questions_data)} questions to import")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Track companies and topics to avoid duplicates
        company_cache = {}
        topic_cache = {}
        
        for idx, q_data in enumerate(questions_data, 1):
            print(f"Importing {idx}/{len(questions_data)}: {q_data['title'][:50]}...")
            
            # Create question
            question = Question(
                title=q_data.get('title'),
                title_slug=q_data.get('titleSlug'),
                difficulty=q_data.get('difficulty'),
                content=q_data.get('content'),
                category=q_data.get('category'),
                source=q_data.get('source'),
                url=q_data.get('url'),
                ac_rate=q_data.get('acRate'),
                scraped_at=q_data.get('scrapedAt')
            )
            
            # Handle companies
            if q_data.get('companyTags'):
                for company_data in q_data['companyTags']:
                    company_name = company_data.get('name') if isinstance(company_data, dict) else company_data
                    
                    if company_name:
                        if company_name not in company_cache:
                            company = db.query(Company).filter(Company.name == company_name).first()
                            if not company:
                                company = Company(name=company_name)
                                db.add(company)
                                db.flush()
                            company_cache[company_name] = company
                        
                        question.companies.append(company_cache[company_name])
            
            # Handle topics
            if q_data.get('topicTags'):
                for topic_data in q_data['topicTags']:
                    topic_name = topic_data.get('name')
                    topic_slug = topic_data.get('slug')
                    
                    if topic_name and topic_slug:
                        if topic_slug not in topic_cache:
                            topic = db.query(Topic).filter(Topic.slug == topic_slug).first()
                            if not topic:
                                topic = Topic(name=topic_name, slug=topic_slug)
                                db.add(topic)
                                db.flush()
                            topic_cache[topic_slug] = topic
                        
                        question.topics.append(topic_cache[topic_slug])
            
            db.add(question)
            
            # Commit every 50 questions
            if idx % 50 == 0:
                db.commit()
                print(f"  ✓ Committed {idx} questions")
        
        # Final commit
        db.commit()
        
        print("\n" + "="*60)
        print("✅ DATA IMPORT COMPLETE!")
        print("="*60)
        print(f"Imported {len(questions_data)} questions")
        print(f"Companies: {len(company_cache)}")
        print(f"Topics: {len(topic_cache)}")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error during import: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import_questions()