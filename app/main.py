from fastapi import FastAPI
from app.api.endpoints import user, parking_slot, booking, feedback
from app.db.session import engine
from app.db.base import Base


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(parking_slot.router, prefix="/parking-slots", tags=["parking-slots"])
app.include_router(booking.router, prefix="/bookings", tags=["bookings"])
app.include_router(feedback.router, prefix="/feedbacks", tags=["feedbacks"])
