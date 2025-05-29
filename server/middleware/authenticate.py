from fastapi import HTTPException, status, Request
from functools import wraps
import jwt
from config import AppConfig, ConfigKeys


def authenticate(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")
        if not request:
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
        if not request:
            raise RuntimeError("Request parameter is required in route handler")

        # Try to get token from cookie first
        token = request.cookies.get("access_token")

        # If not found in cookie, try Authorization header
        if not token:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            raise HTTPException(status_code=401, detail="Authorization token missing")

        try:
            payload = jwt.decode(
                token,
                AppConfig.get(ConfigKeys.JWT_SECRET),
                algorithms=[AppConfig.get(ConfigKeys.JWT_ALGORITHM)]
            )
            request.state.user_id = payload.get("user_id")
            request.state.jwt_payload = payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

        return await func(*args, **kwargs)

    return wrapper

