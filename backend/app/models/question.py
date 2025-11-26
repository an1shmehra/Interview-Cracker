from sqlalchemy import Column, Integer, String, Text, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# Many-to-many relationship tables
question_companies = Table(
    'question_companies',
    Base.metadata,
    Column('question_id', Integer, ForeignKey('questions.id', ondelete='CASCADE'), primary_key=True),
    Column('company_id', Integer, ForeignKey('companies.id', ondelete='CASCADE'), primary_key=True)
)

question_topics = Table(
    'question_topics',
    Base.metadata,
    Column('question_id', Integer, ForeignKey('questions.id', ondelete='CASCADE'), primary_key=True),
    Column('topic_id', Integer, ForeignKey('topics.id', ondelete='CASCADE'), primary_key=True)
)

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False, index=True)
    title_slug = Column(Text, index=True, unique=True)
    difficulty = Column(String(50))
    content = Column(Text)
    category = Column(String(100), index=True)  # DSA, System Design, Behavioral
    source = Column(String(200))
    url = Column(String(1000))
    ac_rate = Column(Float, nullable=True)  # Only for LeetCode
    scraped_at = Column(String(100))
    
    # Relationships
    companies = relationship("Company", secondary=question_companies, back_populates="questions")
    topics = relationship("Topic", secondary=question_topics, back_populates="questions")

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False, index=True)
    
    # Relationships
    questions = relationship("Question", secondary=question_companies, back_populates="companies")

class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, index=True)
    
    # Relationships
    questions = relationship("Question", secondary=question_topics, back_populates="topics")