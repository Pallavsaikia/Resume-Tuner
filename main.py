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


RESUME_STATIC_DIR = os.path.join(os.getcwd(), "resume_serve")
os.makedirs(RESUME_STATIC_DIR, exist_ok=True) 
print(RESUME_STATIC_DIR)
AppConfig.set(ConfigKeys.JWT_SECRET,os.getenv("JWT_SECRET"))
AppConfig.set(ConfigKeys.JWT_ALGORITHM,"HS256")
AppConfig.set(ConfigKeys.RESUME_TEMPLATE,"templates/ats.docx")
AppConfig.set(ConfigKeys.ACCESS_TOKEN_EXPIRE_MINUTES,30)
AppConfig.set(ConfigKeys.RESUME_STATIC_DIR,RESUME_STATIC_DIR)


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


app.include_router(v1_router)