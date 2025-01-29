from pathlib import Path
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("TOKEN")
api_key = os.getenv("API_KEY")

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "db.sqlite3"


class DbSettings(BaseSettings):
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    echo: bool = True


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db: DbSettings = DbSettings()


settings = Settings()
