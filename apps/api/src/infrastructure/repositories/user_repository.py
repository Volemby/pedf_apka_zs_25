from typing import Optional
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from ...infrastructure.orm.models import User
from ...core.database import SessionLocal

def get_by_email(email: str) -> Optional[User]:
    with SessionLocal() as db:
        stmt = select(User).where(User.email == email)
        return db.execute(stmt).scalar_one_or_none()

def get_by_id(user_id: str) -> Optional[User]:
    with SessionLocal() as db:
        stmt = select(User).where(User.id == user_id)
        return db.execute(stmt).scalar_one_or_none()

def create_user(email: str, password_hash: str, role: str = "artist") -> User:
    with SessionLocal() as db:
        stmt = insert(User).values(
            email=email, password_hash=password_hash, role=role
        ).returning(User)
        user = db.execute(stmt).scalar_one()
        db.commit()
        return user
