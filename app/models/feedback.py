from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)

    user = relationship("User", back_populates="feedbacks")
    booking = relationship("Booking", back_populates="feedbacks")
