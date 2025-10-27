from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import ENUM as PGEnum

from src.presentation.routes.auth import auth_router
from src.infrastructure.orm.models import Base
from src.domain.enums import Role, ArtStatus, PrintStatus
from src.core.database import engine

app = FastAPI(title="Appka API")

app.include_router(auth_router, prefix="/auth")

@app.on_event("startup")
def startup():
    # create tables for dev mode
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS citext"))
        PGEnum(Role, name="role", create_type=True).create(bind=conn, checkfirst=True)
        PGEnum(ArtStatus, name="art_status", create_type=True).create(bind=conn, checkfirst=True)
        PGEnum(PrintStatus, name="print_status", create_type=True).create(bind=conn, checkfirst=True)
        Base.metadata.create_all(bind=conn)
