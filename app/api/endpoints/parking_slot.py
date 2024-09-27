from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud import parking_slot as parking_slot_crud
from app.models import user, parking_slot as parking_slot_model
from app.schemas.parking_slot import ParkingSlot, ParkingSlotCreate
from app.api import dependencies


router = APIRouter()


@router.get("/", response_model=List[ParkingSlot])
def get_available_parking_slots(db: Session = Depends(dependencies.get_db), current_user: user.User = Depends(dependencies.get_current_active_user)):
    return parking_slot_crud.get_available_parking_slots(db=db)


# Only accessible by ADMIN
@router.post("/", response_model=ParkingSlot)
def create_parking_slot(slot: ParkingSlotCreate, db: Session = Depends(dependencies.get_db), current_user: user.User = Depends(dependencies.get_current_active_admin)):
    return parking_slot_crud.create_parking_slot(db, slot=slot)


@router.delete("/{slot_id}", response_model=ParkingSlot)
def delete_parking_slot(slot_id: int, db: Session = Depends(dependencies.get_db), current_user: user.User = Depends(dependencies.get_current_active_admin)):
    parking_slot = parking_slot_crud.get_parking_slot(db, slot_id)
    if not parking_slot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parking slot not found")
    return parking_slot_crud.delete_parking_slot(db, slot_id=slot_id)


@router.put("/{slot_id}", response_model=ParkingSlot)
def move_parking_slot_to_maintenance(slot_id: int, db: Session = Depends(dependencies.get_db), current_user: user.User = Depends(dependencies.get_current_active_admin)):
    parking_slot = parking_slot_crud.get_parking_slot(db, slot_id)
    if not parking_slot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parking slot not found")
    return parking_slot_crud.update_parking_slot_status(db, slot_id=slot_id, status=parking_slot_model.ParkingSlotStatus.UNDER_MAINTENANCE)
