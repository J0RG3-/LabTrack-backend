from pydantic import BaseModel, EmailStr
from typing import Literal
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    email: EmailStr
    role: Literal["admin", "visitor"] = "visitor"

class UserOut(BaseModel):
    id: int
    username: str
    name: str
    email: EmailStr
    role: str
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"