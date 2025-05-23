from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database.models import Base, engine, SessionLocal, User

# table 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI() # entry point

# DB session을 가져옵니다.
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@app.post("/test/users/")
def create_user(user: str, content: str, db: Session = Depends(get_db)):
  user = User(
    email="test@gmail.com",
    password="test_password",
    nickname="test_nickname"
  )
  db.add(user)
  db.commit()
  db.refresh(user)
  return user

@app.get("/test/users/")
def get_users(db: Session = Depends(get_db)):
  return db.query(User).all()