from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud import booking as booking_crud
from app.crud import parking_slot
from app.models.parking_slot import ParkingSlotStatus
from app.models import user as user_model
from app.schemas import booking as booking_schema
from app.api import dependencies


router = APIRouter()


@router.post("/", response_model=booking_schema.Booking)
def create_booking(booking: booking_schema.BookingCreate, db: Session = Depends(dependencies.get_db), current_user: user_model.User = Depends(dependencies.get_current_active_user)):
    slot = parking_slot.get_parking_slot(db=db, slot_id=booking.slot_id)
    if slot.status != ParkingSlotStatus.AVAILABLE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parking slot already occupied")
    return booking_crud.create_booking(db=db, booking=booking, user_id=current_user.id)


@router.get("/", response_model=List[booking_schema.Booking])
def get_all_bookings_of_user(db: Session = Depends(dependencies.get_db), current_user: user_model.User = Depends(dependencies.get_current_active_user)):
    return booking_crud.get_bookings_by_user(db=db, user_id=current_user.id)


@router.put("/{booking_id}", response_model=booking_schema.Booking)
def checkout(booking_id: int, db: Session = Depends(dependencies.get_db), current_user: user_model.User = Depends(dependencies.get_current_active_user)):
    booking = booking_crud.get_booking(db, booking_id)
    if not booking or booking.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    slot = parking_slot.get_parking_slot(db=db, slot_id=booking.slot_id)
    if slot.status != ParkingSlotStatus.OCCUPIED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parking slot not occupied")
    parking_slot.update_parking_slot_status(db, slot.id, ParkingSlotStatus.AVAILABLE)
    return booking


@router.delete("/{booking_id}", response_model=booking_schema.Booking)
def cancel_booking(booking_id: int, db: Session = Depends(dependencies.get_db), current_user: user_model.User = Depends(dependencies.get_current_active_user)):
    booking = booking_crud.get_booking(db, booking_id)
    if not booking or booking.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    slot = parking_slot.get_parking_slot(db=db, slot_id=booking.slot_id)
    if slot.status != ParkingSlotStatus.OCCUPIED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parking slot not occupied")
    return booking_crud.delete_booking(db, booking)
