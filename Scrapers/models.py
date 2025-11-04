from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    question_text = Column(Text)
    company = Column(String(100))
    source_url = Column(String(500))

def get_session(db_url="sqlite:///db.sqlite"):
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()
