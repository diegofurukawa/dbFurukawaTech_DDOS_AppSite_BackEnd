# customer_mo_model.py
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class CustomerMOBase(BaseModel):
    idMogid: str
    idCustomer: int
    active: bool = Field(default=True)

class CustomerMOCreate(CustomerMOBase):
    pass

class CustomerMOUpdate(BaseModel):
    idCustomer: Optional[int] = None
    active: Optional[bool] = None

class CustomerMOResponse(CustomerMOBase):
    mo_name: str
    customer_name: str
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True