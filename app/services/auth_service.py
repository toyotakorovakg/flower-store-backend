from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
# ИСПРАВЛЕНИЕ: Правильный путь до вашей модели (app -> db -> models -> customer)
from app.db.models.customer import Customer
from app.schemas.auth import UserCreate, Token
from app.core import security
from app.core.config import settings

async def register_service(user_in: UserCreate, db: AsyncSession) -> Token:
    # 1. Хешируем email для проверки существования и сохранения
    email_hash_bytes = security.hash_email(user_in.email)

    # 2. Проверяем, существует ли пользователь (по хешу email)
    query = select(Customer).where(Customer.email_hash == email_hash_bytes)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # 3. Подготавливаем данные для БД (конвертируем строки в байты/шифротекст)
    
    # Хешируем пароль и получаем bytes
    password_hash_bytes = security.get_password_hash(user_in.password)
    
    # Шифруем PII данные (Full Name, Phone, Address) в bytes
    full_name_enc = security.encrypt_data(user_in.full_name)
    phone_enc = security.encrypt_data(user_in.phone)
    address_enc = security.encrypt_data(user_in.address)

    # 4. Создаем объект модели
    new_customer = Customer(
        email_hash=email_hash_bytes,
        password_hash=password_hash_bytes,
        full_name_enc=full_name_enc,
        phone_enc=phone_enc,
        address_enc=address_enc,
        is_active=True,
        is_verified=False,
        password_algo="bcrypt" 
    )

    # 5. Сохраняем в БД
    db.add(new_customer)
    try:
        await db.commit()
        await db.refresh(new_customer)
    except Exception as e:
        await db.rollback()
        # Логируем ошибку в консоль, чтобы видеть детали если что-то пойдет не так
        print(f"Error creating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user record"
        )

    # 6. Генерируем токен
    access_token = security.create_access_token(subject=new_customer.id)

    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=str(new_customer.id)
    )

async def login_service(user_in: UserCreate, db: AsyncSession):
    email_hash_bytes = security.hash_email(user_in.email)
    
    query = select(Customer).where(Customer.email_hash == email_hash_bytes)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        return None
        
    if not security.verify_password(user_in.password, user.password_hash):
        return None
        
    return user