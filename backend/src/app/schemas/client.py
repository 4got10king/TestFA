from pydantic import BaseModel, EmailStr
from typing import Optional
from .enums import GenderEnum


class ClientFullData(BaseModel):
    id: Optional[int]
    email: EmailStr
    avatar: Optional[bytes] = None
    gender: Optional[GenderEnum]
    name: str
    surname: Optional[str]
    password: str

    class Config:
        from_attributes = True


class ClientData(BaseModel):
    avatar: Optional[bytes] = None
    gender: Optional[GenderEnum]
    name: str
    surname: Optional[str]
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    gender: str
