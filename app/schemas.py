from pydantic import BaseModel
from typing import Optional
from .models import UserRole

class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[UserRole] = UserRole.user

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[UserRole] = None
