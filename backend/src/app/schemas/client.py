from pydantic import BaseModel, EmailStr
from typing import Optional
from .enums import GenderEnum


class ClientFullData(BaseModel):
    id: Optional[int]
    email: EmailStr
    avatar: Optional[bytes]
    gender: Optional[GenderEnum]
    name: str
    surname: Optional[str]

    class Config:
        from_attributes = True


class ClientData(BaseModel):
    avatar: Optional[bytes]
    gender: Optional[GenderEnum]
    name: str
    surname: Optional[str]
    email: EmailStr

    class Config:
        from_attributes = True
