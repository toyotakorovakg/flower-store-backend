from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# --- TOKEN SCHEMAS ---

# Базовая схема токена
class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str

# Эндпоинт ждет TokenResponse, делаем его наследником Token
class TokenResponse(Token):
    pass

# Данные внутри токена (для декодирования)
class TokenData(BaseModel):
    user_id: Optional[str] = None


# --- USER SCHEMAS ---

class UserBase(BaseModel):
    email: EmailStr

# Схема для логина
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Схема для регистрации (используется в api/v1/endpoints/auth.py)
class RegisterRequest(UserBase):
    password: str = Field(..., min_length=8)
    full_name: str
    phone: str
    address: str

# Схема для создания пользователя (используется в services/auth_service.py)
# Мы делаем её просто алиасом (наследником) RegisterRequest, чтобы они были идентичны
class UserCreate(RegisterRequest):
    pass

# Схема для возврата данных пользователя (без пароля)
class User(UserBase):
    id: str
    is_active: bool
    
    class Config:
        from_attributes = True