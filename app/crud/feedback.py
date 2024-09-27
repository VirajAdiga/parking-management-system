from sqlalchemy.orm import Session
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate


def create_feedback(db: Session, feedback: FeedbackCreate, user_id: int):
    db_feedback = Feedback(**feedback.dict(), user_id=user_id)
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


def get_feedbacks_by_user(db: Session, user_id: int):
    return db.query(Feedback).filter(Feedback.user_id == user_id).all()


def get_feedbacks_by_booking(db: Session, booking_id: int):
    return db.query(Feedback).filter(Feedback.booking_id == booking_id).all()
