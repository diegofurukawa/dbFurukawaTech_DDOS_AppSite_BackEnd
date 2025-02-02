# managed_object_model.py
from typing import Optional
from pydantic import BaseModel

class ManagedObjectResponse(BaseModel):
    gid: str
    name: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True