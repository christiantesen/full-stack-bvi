from decouple import config
from functools import lru_cache
from pydantic_settings import BaseSettings
from urllib.parse import quote_plus

class Settings(BaseSettings):

    # App
    APP_NAME:  str = config("APP_NAME", cast=str, default="FastAPI")
    DEBUG: bool = config("DEBUG", cast=bool, default=True)

    # FrontEnd Application
    FRONTEND_HOST: str = config("FRONTEND_HOST", cast=str, default="http://localhost:3000")
    
    # MySql Database Config
    MYSQL_HOST: str = config("MYSQL_HOST", cast=str, default='localhost')
    MYSQL_USER: str = config("MYSQL_USER", cast=str, default='root')
    MYSQL_PASS: str = config("MYSQL_PASSWORD", cast=str, default='secret')
    MYSQL_PORT: int = config("MYSQL_PORT", cast=int, default=3306)
    MYSQL_DB: str = config("MYSQL_DB", cast=str, default='fastapi')
    DATABASE_URI: str = f"mysql+pymysql://{MYSQL_USER}:{quote_plus(MYSQL_PASS)}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

    # JWT Secret Key
    JWT_SECRET: str = config("JWT_SECRET", cast=str, default="649fb93ef34e4fdf4187709c84d643dd61ce730d91856418fdcf563f895ea40f")
    JWT_ALGORITHM: str = config("ACCESS_TOKEN_ALGORITHM", cast=str, default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", 3)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = config("REFRESH_TOKEN_EXPIRE_MINUTES", 1440)

    # Email Config
    SMTP_USER: str = config("SMTP_USER", cast=str, default="")
    SMTP_PASSWORD: str = config("SMTP_PASSWORD", cast=str, default="")
    SMTP_HOST: str = config("SMTP_HOST", cast=str, default="smtp.gmail.com")
    SMTP_PORT: int = config("SMTP_PORT", cast=int, default=587)
    SMTP_TLS: bool = config("SMTP_TLS", cast=bool, default=True)
    SMTP_SSL: bool = config("SMTP_SSL", cast=bool, default=False)

    # App Secret Key
    SECRET_KEY: str = config("SECRET_KEY", cast=str, default="8deadce9449770680910741063cd0a3fe0acb62a8978661f421bbcbb66dc41f1")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
