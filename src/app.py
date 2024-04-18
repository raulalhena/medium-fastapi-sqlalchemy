from fastapi import FastAPI, Depends, status
from typing import List
from db.database import engine, get_db
from users import user_model
from users.user_schemas import UserRequest, UserResponse
from users.user_model import User
from sqlalchemy.orm import Session
from datetime import datetime

app = FastAPI()

user_model.Base.metadata.create_all(bind=engine)

@app.get('/')
def index():
    return { 'message': 'Server alive!', 'time': datetime.now() }

@app.get('/users', status_code=status.HTTP_200_OK, response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    all_users = db.query(User).all()
    return all_users

@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(post_user: UserRequest, db: Session = Depends(get_db)):
    new_user = User(**post_user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user.__dict__