from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# --- TOKEN SCHEMAS ---

# Базовая схема токена
class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str

# Ответ при логине
class TokenResponse(Token):
    pass

# Ответ при регистрации (добавляем этот класс, чтобы исправить ошибку)
class RegisterResponse(Token):
    pass

# Данные внутри токена (для декодирования)
class TokenData(BaseModel):
    user_id: Optional[str] = None


# --- USER SCHEMAS ---

class UserBase(BaseModel):
    email: EmailStr

# Запрос на логин
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Запрос на регистрацию
class RegisterRequest(UserBase):
    password: str = Field(..., min_length=8)
    full_name: str
    phone: str
    address: str

# Алиас для сервиса (UserCreate = RegisterRequest)
class UserCreate(RegisterRequest):
    pass

# Схема пользователя (без пароля)
class User(UserBase):
    id: str
    is_active: bool
    
    class Config:
        from_attributes = True