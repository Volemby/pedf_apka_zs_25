from fastapi import APIRouter, Response, Cookie, HTTPException, status
from typing import Optional
from ...domain.services import user_service
from ...domain.dtos.user import UserCreateDTO, UserAuthDTO, UserDTO
from ...infrastructure.repositories.user_repository import get_by_id

auth_router = APIRouter()
COOKIE_NAME = "access_token"

@auth_router.post("/register", response_model=UserDTO)
def register(dto: UserCreateDTO):
    return user_service.create_user(dto)

@auth_router.post("/login", response_model=UserDTO)
def login(dto: UserAuthDTO, response: Response):
    user = user_service.authenticate(dto)
    token = user_service.create_token(user.id)
    response.set_cookie(COOKIE_NAME, token, httponly=True, samesite="lax")
    return user

@auth_router.get("/me", response_model=UserDTO)
def me(access_token: Optional[str] = Cookie(None, alias=COOKIE_NAME)):
    if not access_token:
        raise HTTPException(status_code=401, detail="No token")
    try:
        data = user_service.decode_token(access_token)
        user = get_by_id(data["sub"])
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user_service._to_dto(user)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid/expired token")

@auth_router.post("/logout")
def logout(response: Response):
    response.delete_cookie(COOKIE_NAME)
    return {"ok": True}
