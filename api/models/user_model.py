# # src/services/api/models/user_model.py
# from typing import Optional
# from datetime import datetime
# from pydantic import BaseModel, EmailStr, constr

# class UserBase(BaseModel):
#     email: EmailStr
#     name: str
#     company: Optional[str] = None
#     role: Optional[str] = None
    
# class UserCreate(UserBase):
#     password: constr(min_length=8)
    
# class UserResponse(UserBase):
#     id: int
#     is_active: bool
#     created_at: datetime
#     last_login: Optional[datetime] = None
    
#     class Config:
#         from_attributes = True

# class UserAccessRequest(BaseModel):
#     email: EmailStr
#     name: str
#     company: str
#     reason: str
#     status: str = "pending"
#     created_at: datetime = datetime.now()


from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, constr

class UserBase(BaseModel):
    email: EmailStr
    name: str
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
    id: int
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True