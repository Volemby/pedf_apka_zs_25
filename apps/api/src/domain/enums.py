from __future__ import annotations

import enum


class Role(str, enum.Enum):
    admin = "admin"
    artist = "artist"
    venue_admin = "venue_admin"
    collector = "collector"
    agent = "agent"
    print_shop = "print_shop"


class ArtStatus(str, enum.Enum):
    draft = "draft"
    active = "active"
    sold = "sold"
    archived = "archived"
    unavailable = "unavailable"


class PrintStatus(str, enum.Enum):
    draft = "draft"
    available = "available"
    sold_out = "sold_out"
    archived = "archived"