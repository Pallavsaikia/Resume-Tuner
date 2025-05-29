from fastapi import APIRouter, HTTPException, status,Response
from pydantic import BaseModel, EmailStr
from server.authentication.service import AuthService
from server.authentication.dto import RegisterRequest,LoginRequest
router = APIRouter(prefix="/auth", tags=["Auth"])




async def register_user(data: RegisterRequest):
    try:
        user = await AuthService.register_user(data.email, data.password, data.name)
        return {"id": user.id, "email": user.email}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


async def login_user(data: LoginRequest,response: Response):
    try:
        token = await AuthService.login_user(data.email, data.password)
        response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,        # set True if using HTTPS
        samesite="lax",     # or "strict", depending on your needs
        max_age=3600        # optional: cookie expiry in seconds
    )
        return {"access_token": token, "token_type": "bearer"}
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
