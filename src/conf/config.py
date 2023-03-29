from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_url: str = "db_URL"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
