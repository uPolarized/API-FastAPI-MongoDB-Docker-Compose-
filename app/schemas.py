# app/schemas.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from objectid import PyObjectId


class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=80, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    age: int = Field(..., ge=0, description="User's age, must be non-negative")
    is_active: bool = Field(default=True, description="Indicates if the user is active")


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=80)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: PyObjectId = Field(alias="_id", default=None)

    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {PyObjectId: str}

class PaginatedUserResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: List[UserResponse]