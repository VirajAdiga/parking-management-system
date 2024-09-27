from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas import feedback as feedback_schema
from app.crud import feedback as feedback_crud
from app.models import user
from app.api import dependencies


router = APIRouter()


@router.post("/", response_model=feedback_schema.Feedback)
def create_feedback(feedback: feedback_schema.FeedbackCreate, db: Session = Depends(dependencies.get_db), current_user: user.User = Depends(dependencies.get_current_active_user)):
    return feedback_crud.create_feedback(db=db, feedback=feedback, user_id=current_user.id)


@router.get("/", response_model=List[feedback_schema.Feedback])
def get_feedbacks_by_user(db: Session = Depends(dependencies.get_db), current_user: user.User = Depends(dependencies.get_current_active_user)):
    return feedback_crud.get_feedbacks_by_user(db=db, user_id=current_user.id)


@router.get("/{booking_id}", response_model=List[feedback_schema.Feedback])
def get_feedbacks_by_booking(booking_id: int, db: Session = Depends(dependencies.get_db), current_user: user.User = Depends(dependencies.get_current_active_user)):
    return feedback_crud.get_feedbacks_by_booking(db=db, booking_id=booking_id)
