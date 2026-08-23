from pydantic import BaseModel, EmailStr, Field
from typing import Literal


class UserBase(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    role: Literal["admin", "support", "user"]
    is_active: bool


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int