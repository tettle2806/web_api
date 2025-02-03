from pathlib import Path
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")
TOKEN = os.getenv("BOT_TOKEN")
api_key = os.getenv("API_KEY")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
JWT_REFRESH_SECRET_KEY = os.environ["JWT_REFRESH_SECRET_KEY"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

BASE_DIR = Path(__file__).parent.parent
DB_URL = os.getenv("DB_URL")


class DbSettings(BaseSettings):
    url: str = DB_URL
    echo: bool = True


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db: DbSettings = DbSettings()


settings = Settings()
