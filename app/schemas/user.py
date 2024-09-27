from enum import Enum

from pydantic import BaseModel


class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class UserBase(BaseModel):
    username: str
    email: str
    role: UserRole = UserRole.USER


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
