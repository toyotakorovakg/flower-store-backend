from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# Основная схема токена
class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str

# Добавляем TokenResponse как наследника Token, чтобы удовлетворить импорт
class TokenResponse(Token):
    pass

# Данные внутри токена
class TokenData(BaseModel):
    user_id: Optional[str] = None

# Базовая схема пользователя
class UserBase(BaseModel):
    email: EmailStr

# Схема для запроса логина
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Схема для регистрации
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    full_name: str
    phone: str
    address: str

# Схема для отображения пользователя
class User(UserBase):
    id: str
    is_active: bool
    
    class Config:
        from_attributes = True