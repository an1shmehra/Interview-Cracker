from pydantic import BaseModel
from typing import List, Optional

class TopicBase(BaseModel):
    name: str
    slug: str

class Topic(TopicBase):
    id: int
    
    class Config:
        from_attributes = True

class CompanyBase(BaseModel):
    name: str

class Company(CompanyBase):
    id: int
    
    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    title: str
    title_slug: Optional[str] = None
    difficulty: Optional[str] = None
    content: Optional[str] = None
    category: str
    source: Optional[str] = None
    url: Optional[str] = None
    ac_rate: Optional[float] = None

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    companies: List[Company] = []
    topics: List[Topic] = []
    
    class Config:
        from_attributes = True

class QuestionList(BaseModel):
    total: int
    questions: List[Question]