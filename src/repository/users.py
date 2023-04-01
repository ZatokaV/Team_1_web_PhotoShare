from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_profile(username: str, db: Session) -> UserModel:
    pass


async def get_all_users(user: User, db: Session):
    all_users = db.query(User).filter(and_(user.id == 1)).all()
    return all_users
