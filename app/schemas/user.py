from pydantic import BaseModel, EmailStr
from enum import Enum


class RoleEnum(str, Enum):
    admin = "admin"
    teacher = "teacher"
    etudiant = "etudiant"


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: RoleEnum

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool


class UserAuth(BaseModel):
    email: EmailStr
    password: str