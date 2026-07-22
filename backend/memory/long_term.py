from database.connection import SessionLocal
from database.models import UserProgress
from datetime import datetime


def save_progress(user_id: str, resume_ats_score: float = None, weak_topics: list = None, session_summary: str = None):
    db = SessionLocal()
    try:
        progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()

        if progress is None:
            progress = UserProgress(user_id=user_id)
            db.add(progress)

        if resume_ats_score is not None:
            progress.resume_ats_score = resume_ats_score
        if weak_topics is not None:
            progress.weak_topics = ", ".join(weak_topics)
        if session_summary is not None:
            progress.last_session_summary = session_summary

        progress.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(progress)
        return progress
    finally:
        db.close()


def get_progress(user_id: str):
    db = SessionLocal()
    try:
        progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()
        if progress is None:
            return None
        return {
            "user_id": progress.user_id,
            "resume_ats_score": progress.resume_ats_score,
            "weak_topics": progress.weak_topics.split(", ") if progress.weak_topics else [],
            "last_session_summary": progress.last_session_summary,
            "updated_at": progress.updated_at.isoformat() if progress.updated_at else None
        }
    finally:
        db.close()
