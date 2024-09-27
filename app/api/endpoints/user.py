from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.crud import user as user_crud
from app.schemas import user as user_schema
from app.api import dependencies
from app.core.security import create_access_token, verify_password
from app.core.config import settings
from app.models.user import User


router = APIRouter()


@router.post("/register", response_model=user_schema.User)
def register_user(user: user_schema.UserCreate, db: Session = Depends(dependencies.get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    db_user = user_crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    return user_crud.create_user(db=db, user=user)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(dependencies.get_db)):
    user = user_crud.get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


# Only accessible by ADMIN
@router.delete("/{user_id}", response_model=user_schema.User)
def delete_user(user_id: int, db: Session = Depends(dependencies.get_db), current_user: User = Depends(dependencies.get_current_active_admin)):
    db_user = user_crud.get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_crud.delete_user(db, user_id=user_id)
