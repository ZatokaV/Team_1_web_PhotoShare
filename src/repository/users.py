from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_profile(username: str, db: Session) -> UserModel:
    pass
