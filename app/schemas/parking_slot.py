from pydantic import BaseModel
from enum import Enum


class ParkingSlotStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"
    UNDER_MAINTENANCE = "UNDER_MAINTENANCE"


class ParkingSlotBase(BaseModel):
    label: str
    status: ParkingSlotStatus = ParkingSlotStatus.AVAILABLE


class ParkingSlotCreate(ParkingSlotBase):
    pass


class ParkingSlot(ParkingSlotBase):
    id: int

    class Config:
        orm_mode = True
