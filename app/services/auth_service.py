from typing import Optional, Dict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from app.db.models.customer import Customer
from app.schemas.auth import UserCreate, Token
from app.core import security


async def register_user(
    db: AsyncSession,
    *,
    email: str,
    password: str,
    full_name: str,
    phone: str,
    address: str,
) -> Dict[str, str]:
    """
    Создаёт нового клиента и возвращает словарь с токеном. Ограничивает
    длину пароля до 72 байт, поскольку bcrypt не обрабатывает более длинные
    строки:contentReference[oaicite:1]{index=1}.
    """
    if len(password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password too long. Maximum length is 72 characters.",
        )

    # Проверяем, существует ли пользователь
    email_hash = security.hash_email(email)
    result = await db.execute(select(Customer).where(Customer.email_hash == email_hash))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    # Хешируем пароль и шифруем PII
    password_hash = security.get_password_hash(password)
    full_name_enc = security.encrypt_data(full_name)
    phone_enc = security.encrypt_data(phone)
    address_enc = security.encrypt_data(address)

    # Создаём и сохраняем клиента
    new_customer = Customer(
        email_hash=email_hash,
        password_hash=password_hash,
        full_name_enc=full_name_enc,
        phone_enc=phone_enc,
        address_enc=address_enc,
        is_active=True,
        is_verified=False,
        password_algo="bcrypt",
    )
    db.add(new_customer)
    try:
        await db.commit()
        await db.refresh(new_customer)
    except Exception as exc:
        await db.rollback()
        print(f"Error creating user: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user record",
        )

    # Генерируем JWT
    access_token = security.create_access_token(subject=new_customer.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(new_customer.id),
    }


async def register_service(user_in: UserCreate, db: AsyncSession) -> Token:
    """
    Обёртка для совместимости со старой сигнатурой (принимает UserCreate).
    """
    token_dict = await register_user(
        db=db,
        email=user_in.email,
        password=user_in.password,
        full_name=user_in.full_name,
        phone=user_in.phone,
        address=user_in.address,
    )
    return Token(**token_dict)


async def login(
    db: AsyncSession,
    email: str,
    password: str,
) -> Optional[Dict[str, str]]:
    """
    Аутентифицирует пользователя и возвращает словарь с токеном. Возвращает None,
    если пользователь не найден или пароль неверный.
    """
    email_hash = security.hash_email(email)
    result = await db.execute(select(Customer).where(Customer.email_hash == email_hash))
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
    Обёртка для совместимости: принимает UserCreate и вызывает login.
    """
    return await login(db, user_in.email, user_in.password)
