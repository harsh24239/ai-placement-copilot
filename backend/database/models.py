from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database.connection import Base


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    resume_ats_score = Column(Float, nullable=True)
    weak_topics = Column(String, nullable=True)
    last_session_summary = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    credits_remaining = Column(Integer, default=20)
    created_at = Column(DateTime, default=datetime.utcnow)
