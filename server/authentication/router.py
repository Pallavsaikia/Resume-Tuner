from fastapi import APIRouter,Response
from server.authentication.controller import register_user,login_user
from server.authentication.dto import RegisterRequest,LoginRequest
from server.middleware.authenticate import authenticate
from fastapi import Request

router = APIRouter(prefix="/auth", tags=["Users"])

@router.post("/register")
async def register(data: RegisterRequest):
    return await register_user(data)

@router.post("/login")
async def register(data: LoginRequest,response:Response):
    return await login_user(data,response)


@router.post("/test")
@authenticate
async def y(request: Request):
     return {"user_id": request.state.user_id}

