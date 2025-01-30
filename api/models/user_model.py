from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, constr

class UserBase(BaseModel):
    email: EmailStr
    nameUser: str
    company: Optional[str] = None
    role: Optional[str] = None

class UserCreate(UserBase):
    password: constr(min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

class UserResponse(UserBase):
    idUser: int
    active: bool
    createdAt: datetime
    updatedAt: Optional[datetime] = None
    lastLogin: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    nameUser: Optional[str] = None
    company: Optional[str] = None
    role: Optional[str] = None
    password: Optional[constr(min_length=8)] = None
    active: Optional[bool] = None

    class Config:
        from_attributes = True