import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext

from ...infrastructure.repositories import user_repository
from ...domain.dtos.user import UserCreateDTO, UserAuthDTO, UserDTO

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "dev_secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _hash_password(password: str) -> str:
    return pwd_context.hash(password)

def _verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def _to_dto(user) -> UserDTO:
    return UserDTO(id=str(user.id), email=user.email, role=user.role)

def create_user(dto: UserCreateDTO) -> UserDTO:
    existing = user_repository.get_by_email(dto.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = _hash_password(dto.password)
    user = user_repository.create_user(dto.email, hashed, dto.role)
    return _to_dto(user)

def authenticate(dto: UserAuthDTO) -> UserDTO:
    user = user_repository.get_by_email(dto.email)
    if not user or not _verify_password(dto.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return _to_dto(user)

def create_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
