from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_profile(username: str, db: Session) -> UserModel:
    pass


async def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()


async def get_all_users(user: User, db: Session):
    all_users = db.query(User).filter(and_(user.id == 1)).all()
    return all_users


async def create_user(body: UserModel, db: Session) -> User:
    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()
