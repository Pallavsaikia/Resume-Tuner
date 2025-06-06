import os


class ConfigKeys:
    JWT_SECRET = "JWT_SECRET"
    JWT_ALGORITHM = "JWT_ALGORITHM"
    ACCESS_TOKEN_EXPIRE_MINUTES="ACCESS_TOKEN_EXPIRE_MINUTES"
    RESUME_STATIC_DIR="RESUME_STATIC_DIR"
    RESUME_TEMPLATE="RESUME_TEMPLATE"
class AppConfig:
    _config = {}

    @classmethod
    def set(cls, key: str, value):
        cls._config[key] = value

    @classmethod
    def get(cls, key: str, default=None):
        return cls._config.get(key, default)