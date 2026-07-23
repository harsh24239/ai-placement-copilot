from fastapi import Header, HTTPException
from database.connection import SessionLocal
from database.models import User
from auth.security import decode_access_token


def get_current_user(authorization: str = Header(None)) -> User:
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == int(payload["sub"])).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User no longer exists")
        return user
    finally:
        db.close()
