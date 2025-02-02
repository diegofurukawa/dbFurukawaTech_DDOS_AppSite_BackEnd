# company_model.py
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class CompanyBase(BaseModel):
    nameCompany: str
    emailContact: EmailStr
    phoneNumberContact: Optional[str] = None
    address: Optional[str] = None
    active: bool = Field(default=True)  # Changed to boolean with default True

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    nameCompany: Optional[str] = None
    emailContact: Optional[EmailStr] = None
    phoneNumberContact: Optional[str] = None
    address: Optional[str] = None
    active: Optional[bool] = None  # Changed to Optional[bool]

class CompanyResponse(CompanyBase):
    idCompany: int
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True