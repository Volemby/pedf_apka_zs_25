from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr
from pydantic.config import ConfigDict

from .enums import Role


class UserDTO(BaseModel):
    id: UUID
    email: EmailStr
    role: Role
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreateDTO(BaseModel):
    email: EmailStr
    password: str
    role: Optional[Role] = None


class UserAuthDTO(BaseModel):
    email: EmailStr
    password: str