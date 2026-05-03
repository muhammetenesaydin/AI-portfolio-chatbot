from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String) # Gerçek sistemde hashlenmeli
    full_name = Column(String)
    role = Column(String) # 'hr' or 'candidate'

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String, index=True)
    skills = Column(JSON)
    experience_years = Column(Integer, default=0)
    quiz_score = Column(Integer, nullable=True)
    raw_text = Column(String, nullable=True)

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, index=True)
    questions = Column(JSON)
    correct_answers = Column(JSON)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer)
    receiver_id = Column(Integer)
    content = Column(String)
    created_at = Column(String)
