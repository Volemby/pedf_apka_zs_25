from __future__ import annotations

import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """Declarative base for ORM models."""

    @declared_attr.directive
    def __tablename__(cls) -> str:  # type: ignore[override]
        return cls.__name__.lower()


class TimestampMixin:
    """Common created/updated timestamps for most tables."""

    created_at = sa.Column(
        sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")
    )
    updated_at = sa.Column(
        sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")
    )


class SoftDeleteMixin:
    """Optional deleted_at column for soft-deletable tables."""

    deleted_at = sa.Column(sa.DateTime(timezone=True), nullable=True)
