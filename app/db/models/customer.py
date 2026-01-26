import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Integer, LargeBinary, SmallInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
# Импорт Base из base_class разрывает циклический импорт
from app.db.base_class import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # email_hash хранится как байты
    email_hash = Column(LargeBinary, nullable=False, unique=True, index=True)
    # password_hash хранится как байты
    password_hash = Column(LargeBinary, nullable=False)
    
    password_algo = Column(String, default="bcrypt", nullable=False)
    password_changed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # PII данные хранятся в зашифрованном виде (BYTEA)
    full_name_enc = Column(LargeBinary, nullable=True)
    phone_enc = Column(LargeBinary, nullable=True)
    address_enc = Column(LargeBinary, nullable=True)
    
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    
    failed_login_count = Column(SmallInteger, default=0, nullable=False)
    locked_until = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    version = Column(Integer, default=1, nullable=False)