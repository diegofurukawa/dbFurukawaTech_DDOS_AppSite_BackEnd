# customer_model.py
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class CustomerBase(BaseModel):
    nameCustomer: str
    emailContact: EmailStr
    phoneNumberContact: Optional[str] = None
    address: Optional[str] = None
    active: bool = Field(default=True)  # Changed to boolean with default True
    idCompany: int  # Added Company relationship
    
class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    nameCustomer: Optional[str] = None
    emailContact: Optional[EmailStr] = None
    phoneNumberContact: Optional[str] = None
    address: Optional[str] = None
    active: Optional[bool] = None  # Changed to Optional[bool]
    idCompany: Optional[int] = None  # Added Company relationship

class CustomerResponse(CustomerBase):
    idCustomer: int
    idCompany: int  # Assegure-se que este campo existe
    nameCompany: Optional[str] = None #Campo para formulario de Clientes
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True