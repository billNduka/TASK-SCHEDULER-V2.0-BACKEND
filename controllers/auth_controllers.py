from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserOut, UserLogin
from models.models import User
from database import SessionLocal
from core.security import hash_password, verify_password, create_access_token
from sqlalchemy.orm import Session

def register_user(user: UserCreate, db: Session):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserOut(id=new_user.id, username=new_user.username, email=new_user.email)

def login_user(user: UserLogin, db: Session):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}