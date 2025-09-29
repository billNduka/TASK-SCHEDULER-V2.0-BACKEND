from fastapi import APIRouter, Depends
from controllers.auth_controllers import register_user, login_user
from schemas.user import UserCreate, UserLogin, UserOut
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(user, db)