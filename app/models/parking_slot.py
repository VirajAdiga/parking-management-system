import enum

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class ParkingSlotStatus(enum.Enum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"
    UNDER_MAINTENANCE = "UNDER_MAINTENANCE"


class ParkingSlot(Base):
    __tablename__ = "parking_slots"
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, unique=True, index=True)
    status = Column(Enum(ParkingSlotStatus), default=ParkingSlotStatus.AVAILABLE)

    bookings = relationship("Booking", back_populates="slot")
