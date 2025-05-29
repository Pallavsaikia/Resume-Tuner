# models.py

from tortoise.models import Model
from tortoise import fields
from pydantic import BaseModel
from datetime import datetime


class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=100, unique=True)
    name = fields.CharField(max_length=100)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"


class UserCreate(BaseModel):
    email: str
    name: str
    is_active: bool = True


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
