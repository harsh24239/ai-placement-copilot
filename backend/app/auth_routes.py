from fastapi import APIRouter, HTTPException
from database.connection import SessionLocal
from database.models import User
from models.user import SignupRequest, LoginRequest, TokenResponse
from auth.security import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/auth/signup", response_model=TokenResponse)
def signup(request: SignupRequest):
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == request.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="An account with this email already exists")

        new_user = User(
            email=request.email,
            hashed_password=hash_password(request.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        token = create_access_token(new_user.id, new_user.email)
        return TokenResponse(access_token=token, credits_remaining=new_user.credits_remaining)
    finally:
        db.close()


@router.post("/auth/login", response_model=TokenResponse)
def login(request: LoginRequest):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == request.email).first()
        if not user or not verify_password(request.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        token = create_access_token(user.id, user.email)
        return TokenResponse(access_token=token, credits_remaining=user.credits_remaining)
    finally:
        db.close()
