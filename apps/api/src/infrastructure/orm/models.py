from __future__ import annotations

from typing import ClassVar
from datetime import date, datetime
import uuid
import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, CITEXT, ENUM as PGEnum
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, SoftDeleteMixin
from src.domain.enums import Role, ArtStatus, PrintStatus


# =========
# User and profile
# =========

class AppProfile(TimestampMixin, Base):
    __tablename__: ClassVar[str] = "app_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,  # ← generates UUID in Python
    )

class User(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__: ClassVar[str] = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,  # ← generates UUID in Python
    )
    email: Mapped[str] = mapped_column(CITEXT(), unique=True, nullable=False)
    password_hash: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    role: Mapped[Role] = mapped_column(PGEnum(Role, name="role", create_type=False), default=Role.artist)
    phone: Mapped[str | None]
    locale: Mapped[str | None]

class Artist(TimestampMixin, Base):
    __tablename__: ClassVar[str] = "artists"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,  # ← generates UUID in Python
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        unique=True,
        nullable=True,
    )
    profile_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("app_profiles.id"),
        unique=True,
    )
    name: Mapped[str]
    bio: Mapped[str | None]
    year_of_birth: Mapped[int | None]
    location: Mapped[str | None]
    profile_picture_url: Mapped[str | None]
    currency_code: Mapped[str] = mapped_column(sa.Text, default="EUR", nullable=False)

class ArtistPhoto(Base):
    __tablename__: ClassVar[str] = "artist_photos"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,  # ← generates UUID in Python
    )
    artist_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("artists.id"),
        unique=True,
    )
    url: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.text("now()"))


# =========
# Artwork
# =========


class ArtworkMain(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__: ClassVar[str] = "artwork_main"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,  # ← generates UUID in Python
    )
    artist_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("artists.id"),
        nullable=False,
    )
    title: Mapped[str]
    about: Mapped[str | None]
    subject: Mapped[str | None]
    unit: Mapped[str] = mapped_column(sa.Text, default="cm", nullable=False)
    is_3d: Mapped[bool] = mapped_column(sa.Boolean, default=False, nullable=False)
    status: Mapped[ArtStatus] = mapped_column(PGEnum(ArtStatus, name="art_status", create_type=False), default=ArtStatus.draft, nullable=False)
    date_finished: Mapped[date | None]


class ArtOriginal(TimestampMixin, Base):
    __tablename__: ClassVar[str] = "art_original"
    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,  # ← generates UUID in Python
    )
    main_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("artwork_main.id"),
        unique=True,
        nullable=False,
    )
    medium: Mapped[str | None]
    width: Mapped[float | None] = mapped_column(sa.Numeric(10, 2))
    height: Mapped[float | None] = mapped_column(sa.Numeric(10, 2))
    depth: Mapped[float | None] = mapped_column(sa.Numeric(10, 2))
    sale_allowed: Mapped[bool] = mapped_column(sa.Boolean, default=True, nullable=False)
    price_amount: Mapped[float | None] = mapped_column(sa.Numeric(12, 2))


class ArtPrint(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__: ClassVar[str] = "art_print"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,  # ← generates UUID in Python
    )
    main_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("artwork_main.id"),
        nullable=False,
    )
    title: Mapped[str | None]
    medium: Mapped[str | None]
    width: Mapped[float | None] = mapped_column(sa.Numeric(10, 2))
    height: Mapped[float | None] = mapped_column(sa.Numeric(10, 2))
    depth: Mapped[float | None] = mapped_column(sa.Numeric(10, 2))
    price_amount: Mapped[float | None] = mapped_column(sa.Numeric(12, 2))
    print_amount: Mapped[int | None]
    edition_number: Mapped[int | None]
    edition_size: Mapped[int | None]
    status: Mapped[PrintStatus] = mapped_column(PGEnum(PrintStatus, name="print_status", create_type=False), default=PrintStatus.draft, nullable=False)
    sale_allowed: Mapped[bool] = mapped_column(sa.Boolean, default=True, nullable=False)


class ArtworkPhoto(Base):
    __tablename__: ClassVar[str] = "artwork_photos"
    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,  # ← generates UUID in Python
    )
    main_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("artwork_main.id")
    )
    original_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("art_original.id")
    )
    print_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("art_print.id")
    )
    url: Mapped[str]
    is_main: Mapped[bool] = mapped_column(sa.Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.text("now()"))
