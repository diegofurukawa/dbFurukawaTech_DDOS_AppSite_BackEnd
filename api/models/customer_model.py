from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    company: str
    phoneNumber: Optional[str] = None
    address: Optional[str] = None
    status: str = "active"

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    company: Optional[str] = None
    phoneNumber: Optional[str] = None
    address: Optional[str] = None
    status: Optional[str] = None

class CustomerResponse(CustomerBase):
    idCustomer: int
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True