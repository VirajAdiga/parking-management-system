import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    DATABASE_URI: str = os.getenv("DATABASE_URL")
    TEST_DATABASE_URI: str = os.getenv("TEST_DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()
