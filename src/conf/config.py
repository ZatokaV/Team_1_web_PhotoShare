from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_url: str = 'db_URL'
    cloudinary_name: str = 'cloud_name'
    cloudinary_api_key: str = 'api_key'
    cloudinary_api_secret: str = 'api_secret'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
