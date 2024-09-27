import enum

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class UserRole(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.USER)

    bookings = relationship("Booking", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")
