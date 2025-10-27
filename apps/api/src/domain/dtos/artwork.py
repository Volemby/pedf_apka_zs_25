from __future__ import annotations

from datetime import date, datetime
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel
from pydantic.config import ConfigDict

from .enums import OriginalStatus, PrintStatus


class ArtworkMainDTO(BaseModel):
    id: UUID
    artist_id: UUID
    title: str
    about: str | None
    subject: str | None
    unit: str
    is_3d: bool
    date_finished: date | None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class ArtOriginalDTO(BaseModel):
    id: UUID
    main_id: UUID
    status: OriginalStatus
    medium: str | None
    width: Decimal | None
    height: Decimal | None
    depth: Decimal | None
    sale_allowed: bool
    price_amount: Decimal | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ArtPrintDTO(BaseModel):
    id: UUID
    main_id: UUID
    title: str | None
    medium: str | None
    width: Decimal | None
    height: Decimal | None
    depth: Decimal | None
    price_amount: Decimal | None
    print_amount: int | None
    edition_number: int | None
    edition_size: int | None
    status: PrintStatus
    sale_allowed: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class ArtworkPhotoDTO(BaseModel):
    id: UUID
    main_id: UUID | None
    original_id: UUID | None
    print_id: UUID | None
    url: str
    is_main: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

