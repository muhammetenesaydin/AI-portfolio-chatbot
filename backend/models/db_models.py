from sqlalchemy import Column, Integer, String, JSON
from database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    skills = Column(JSON)
    experience_years = Column(Integer, default=0)
    quiz_score = Column(Integer, nullable=True)
    raw_text = Column(String, nullable=True)

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, index=True)
    questions = Column(JSON) # Store list of {"question": "", "options": [], "correct": ""}
