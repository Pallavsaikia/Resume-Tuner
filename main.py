from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise

from server.users.models import UserCreate, UserResponse,User
from database import TortoiseConfig
from dotenv import load_dotenv
import os
from config import AppConfig,ConfigKeys
from server.api.v1.router import router as v1_router
load_dotenv()

app = FastAPI()
app.include_router(v1_router)

UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True) 
print(UPLOAD_DIR)
AppConfig.set(ConfigKeys.JWT_SECRET,os.getenv("JWT_SECRET"))
AppConfig.set(ConfigKeys.JWT_ALGORITHM,"HS256")
AppConfig.set(ConfigKeys.ACCESS_TOKEN_EXPIRE_MINUTES,30)
AppConfig.set(ConfigKeys.UPLOAD_DIR,UPLOAD_DIR)


# Database configuration
TORTOISE_ORM = TortoiseConfig.config(
    username=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    db_name=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT", 5432)),
    debug=True
)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)





# @app.post("/users/", response_model=UserResponse)
# async def create_user(user: UserCreate):
#     user_obj = await User.create(**user.model_dump())
#     return UserResponse.model_validate(user_obj)

# @app.get("/users/{user_id}", response_model=UserResponse)
# async def get_user(user_id: int):
#     user = await User.get_or_none(id=user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return UserResponse.model_validate(user)

# @app.get("/users/", response_model=list[UserResponse])
# async def get_users(skip: int = 0, limit: int = 100):
#     users = await User.all().offset(skip).limit(limit)
#     return [UserResponse.model_validate(user) for user in users]

# @app.put("/users/{user_id}", response_model=UserResponse)
# async def update_user(user_id: int, user_data: UserCreate):
#     user = await User.get_or_none(id=user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     await user.update_from_dict(user_data.model_dump()).save()
#     return UserResponse.model_validate(user)