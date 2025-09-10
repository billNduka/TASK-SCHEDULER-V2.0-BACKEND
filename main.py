from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models.models import User, Task

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db    
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
