from pydantic import BaseModel
from typing import Optional


class FeedbackBase(BaseModel):
    rating: int
    comment: Optional[str] = None


class FeedbackCreate(FeedbackBase):
    booking_id: int


class FeedbackInDbBase(FeedbackBase):
    id: int
    user_id: int
    booking_id: int

    class Config:
        orm_mode = True


class Feedback(FeedbackInDbBase):
    pass
