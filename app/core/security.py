from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt
from passlib.context import CryptContext
import hashlib
import base64
from cryptography.fernet import Fernet
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

# --- Хелпер для шифрования (Fernet) ---
def _get_fernet() -> Fernet:
    """
    Генерирует валидный ключ Fernet на основе ENCRYPTION_KEY из .env.
    Fernet требует 32 url-safe base64 байта. Мы хешируем твой ключ, чтобы получить нужную длину.
    """
    key_bytes = settings.ENCRYPTION_KEY.encode('utf-8')
    # Используем SHA256 чтобы гарантировать 32 байта, затем base64 кодируем
    secure_key = base64.urlsafe_b64encode(hashlib.sha256(key_bytes).digest())
    return Fernet(secure_key)

def encrypt_data(data: Optional[str]) -> Optional[bytes]:
    """Шифрует строку и возвращает байты для БД (BYTEA)"""
    if not data:
        return None
    f = _get_fernet()
    return f.encrypt(data.encode('utf-8'))

def decrypt_data(data: Optional[bytes]) -> Optional[str]:
    """Расшифровывает байты из БД обратно в строку"""
    if not data:
        return None
    f = _get_fernet()
    try:
        return f.decrypt(data).decode('utf-8')
    except Exception:
        return None

# --- Хелперы для хеширования ---

def hash_email(email: str) -> bytes:
    """Хеширует email с солью (pepper) для безопасного поиска. Возвращает bytes."""
    clean_email = email.lower().strip()
    payload = (clean_email + settings.EMAIL_PEPPER).encode("utf-8")
    # Используем SHA256, так как в SQL функции указан digest(..., 'sha256')
    return hashlib.sha256(payload).digest()

def verify_password(plain_password: str, hashed_password_bytes: bytes) -> bool:
    """Проверяет пароль. Принимает хеш в байтах, декодирует его для passlib."""
    try:
        # Passlib работает со строками, поэтому декодируем байты из БД
        hashed_password_str = hashed_password_bytes.decode('utf-8')
        return pwd_context.verify(plain_password, hashed_password_str)
    except Exception:
        return False

def get_password_hash(password: str) -> bytes:
    """Хеширует пароль и возвращает bytes для сохранения в BYTEA колонку."""
    # Получаем строковый хеш от passlib
    hash_str = pwd_context.hash(password)
    # Кодируем в байты для базы данных
    return hash_str.encode('utf-8')

# --- JWT Token ---

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt