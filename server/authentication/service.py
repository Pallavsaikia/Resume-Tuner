import jwt  # ← pyjwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from server.users.models import User
from  config import AppConfig,ConfigKeys
from datetime import timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=AppConfig.get(ConfigKeys.ACCESS_TOKEN_EXPIRE_MINUTES)))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, AppConfig.get(ConfigKeys.JWT_SECRET), algorithm=AppConfig.get(ConfigKeys.JWT_ALGORITHM))

    @classmethod
    async def register_user(cls, email: str, password: str, name: str):
        user = await User.get_or_none(email=email)
        if user:
            raise ValueError("Email already registered")
        hashed_pw = cls.hash_password(password)
        return await User.create(email=email, password=hashed_pw, name=name)

    @classmethod
    async def login_user(cls, email: str, password: str) -> str:
        user = await User.get_or_none(email=email)
        if not user or not cls.verify_password(password, user.password):
            raise ValueError("Invalid credentials")
        return cls.create_access_token({"user_id": user.id})
