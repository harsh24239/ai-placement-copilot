from fastapi import Depends, HTTPException
from database.connection import SessionLocal
from database.models import User
from auth.dependencies import get_current_user


def require_credits(cost: int = 1):
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.credits_remaining < cost:
            raise HTTPException(
                status_code=402,
                detail=f"Not enough credits. You have {current_user.credits_remaining}, this action costs {cost}."
            )

        db = SessionLocal()
        try:
            db_user = db.query(User).filter(User.id == current_user.id).first()
            db_user.credits_remaining -= cost
            db.commit()
            db.refresh(db_user)
            return db_user
        finally:
            db.close()

    return dependency
