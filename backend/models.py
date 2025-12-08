from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class MessageIn(BaseModel):
    text: str
    chat_id: Optional[str] = None

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ChatCreate(BaseModel):
    title: Optional[str] = None

class ChatResponse(BaseModel):
    id: str
    title: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0

class ChatUpdate(BaseModel):
    title: str
