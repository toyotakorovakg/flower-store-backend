from typing import Optional, Dict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from app.db.models.customer import Customer
from app.schemas.auth import UserCreate, Token
from app.core import security
from app.core.config import settings


async def register_user(
    db: AsyncSession,
    *,
    email: str,
    password: str,
    full_name: str,
    phone: str,
    address: str,
) -> dict[str, str]:
    """
    Создаёт нового клиента и возвращает словарь с access_token, token_type и user_id.
    Сигнатура соответствует ожиданиям роутера.
    """
    # 1. Хешируем email и ищем существующего пользователя
    email_hash_bytes = security.hash_email(email)
    query = select(Customer).where(Customer.email_hash == email_hash_bytes)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    # 2. Хешируем пароль и шифруем PII
    password_hash_bytes = security.get_password_hash(password)
    full_name_enc = security.encrypt_data(full_name)
    phone_enc = security.encrypt_data(phone)
    address_enc = security.encrypt_data(address)
    # 3. Создаём запись клиента
    new_customer = Customer(
        email_hash=email_hash_bytes,
        password_hash=password_hash_bytes,
        full_name_enc=full_name_enc,
        phone_enc=phone_enc,
        address_enc=address_enc,
        is_active=True,
        is_verified=False,
        password_algo="bcrypt",
    )
    # 4. Сохраняем в БД
    db.add(new_customer)
    try:
        await db.commit()
        await db.refresh(new_customer)
    except Exception as e:
        await db.rollback()
        print(f"Error creating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user record",
        )
    # 5. Генерируем JWT
    access_token = security.create_access_token(subject=new_customer.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(new_customer.id),
    }


async def register_service(user_in: UserCreate, db: AsyncSession) -> Token:
    """
    Обёртка для обратной совместимости. Принимает UserCreate и возвращает Token.
    """
    token_data = await register_user(
        db=db,
        email=user_in.email,
        password=user_in.password,
        full_name=user_in.full_name,
        phone=user_in.phone,
        address=user_in.address,
    )
    return Token(**token_data)


async def login(
    db: AsyncSession,
    email: str,
    password: str,
) -> Optional[dict[str, str]]:
    """
    Аутентифицирует пользователя. Возвращает словарь с токеном или None.
    """
    email_hash_bytes = security.hash_email(email)
    query = select(Customer).where(Customer.email_hash == email_hash_bytes)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        return None
    if not security.verify_password(password, user.password_hash):
        return None
    access_token = security.create_access_token(subject=user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(user.id),
    }


async def login_service(user_in: UserCreate, db: AsyncSession):
    """
    Обёртка для обратной совместимости. Принимает UserCreate.
    """
    return await login(db, user_in.email, user_in.password)
