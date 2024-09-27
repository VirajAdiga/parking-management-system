from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.schemas.booking import BookingCreate
from app.crud.parking_slot import update_parking_slot_status
from app.models.parking_slot import ParkingSlotStatus


def create_booking(db: Session, booking: BookingCreate, user_id: int):
    db_booking = Booking(**booking.dict(), user_id=user_id)
    update_parking_slot_status(db, db_booking.slot_id, ParkingSlotStatus.OCCUPIED)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_booking(db: Session, booking_id: int):
    return db.query(Booking).filter(Booking.id == booking_id).first()


def get_bookings_by_user(db: Session, user_id: int):
    return db.query(Booking).filter(Booking.user_id == user_id).all()


def delete_booking(db: Session, booking: Booking):
    update_parking_slot_status(db, booking.slot_id, ParkingSlotStatus.AVAILABLE)
    db.delete(booking)
    db.commit()
    return booking
