from pydantic import BaseModel
from datetime import date


class BookingBase(BaseModel):
    slot_id: int
    start_date: date
    end_date: date


class BookingCreate(BookingBase):
    pass


class BookingInDbBase(BookingBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class Booking(BookingInDbBase):
    pass


class BookingInDb(BookingInDbBase):
    pass
