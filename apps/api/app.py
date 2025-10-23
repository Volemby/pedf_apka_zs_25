from fastapi import FastAPI, Depends, HTTPException, status, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy import create_engine, text
import os

#configurations()
# Default DATABASE_URL fallback (user:password).
# Was incorrectly using 'app.app' (missing ':'), which made Postgres try to login as role 'app.app'.
# Correct form is user:password (app:app).
DB_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://app:app@localhost:5432/app")
SESSION_SECRET = os.getenv("SESSION_SECRET", "change_this")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
engine = create_engine(DB_URL, future=True)


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET, same_site="lax", https_only=False)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Bootstrap users table (super simple) ---
with engine.begin() as conn:
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS users (
      id SERIAL PRIMARY KEY,
      email TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL
    );
    """))

# --- Schemas ---
class RegisterIn(BaseModel):
    email: str
    password: str

class LoginIn(BaseModel):
    email: str
    password: str

# --- Helpers ---
def get_user_by_email(email: str):
    with engine.begin() as conn:
        row = conn.execute(text("SELECT id, email, password_hash FROM users WHERE email=:e"), {"e": email}).fetchone()
        return row

def create_user(email: str, password: str):
    hash_ = pwd.hash(password)
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO users (email, password_hash) VALUES (:e, :p)"), {"e": email, "p": hash_})

def require_auth(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user

# --- Routes ---
@app.post("/auth/register")
def register(data: RegisterIn):
    if get_user_by_email(data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    create_user(data.email, data.password)
    return {"ok": True}

@app.post("/auth/login")
def login(data: LoginIn, request: Request, response: Response):
    row = get_user_by_email(data.email)
    if not row or not pwd.verify(data.password, row.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    request.session["user"] = {"id": row.id, "email": row.email}
    return {"ok": True}

@app.post("/auth/logout")
def logout(request: Request):
    request.session.clear()
    return {"ok": True}

@app.get("/auth/me")
def me(user = Depends(require_auth)):
    return {"user": user}

@app.get("/tasks")
def example_protected_resource(user = Depends(require_auth)):
    # return something session-bound
    return {"items": ["task A", "task B"], "email": user["email"]}