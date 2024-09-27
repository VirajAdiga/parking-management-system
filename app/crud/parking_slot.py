from sqlalchemy.orm import Session
from app.models.parking_slot import ParkingSlot, ParkingSlotStatus
from app.schemas.parking_slot import ParkingSlotCreate


def get_parking_slot(db: Session, slot_id: int):
    return db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).first()


def get_available_parking_slots(db: Session):
    return db.query(ParkingSlot).filter(ParkingSlot.status == ParkingSlotStatus.AVAILABLE)


def create_parking_slot(db: Session, slot: ParkingSlotCreate):
    db_slot = ParkingSlot(label=slot.label, status=slot.status)
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot


def update_parking_slot_status(db: Session, slot_id: int, status: ParkingSlotStatus):
    db_slot = db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).first()
    if db_slot:
        db_slot.status = status
        db.commit()
        db.refresh(db_slot)
    return db_slot


def delete_parking_slot(db: Session, slot_id: int):
    db_slot = db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).first()
    if db_slot:
        db.delete(db_slot)
        db.commit()
    return db_slot
