from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import User, Post, UserRole
from src.schemas import UserModel, UserProfileModel
from src.services.messages_templates import PERMISSION_ERROR


async def get_user_profile(username: str, db: Session) -> UserProfileModel:
    this_user = db.query(User).filter(User.username == username).first()
    photo_count = db.query(Post).filter(Post.user == this_user).count()
    user_profile = None
    if this_user:
        user_profile = UserProfileModel(
            id=this_user.id, username=this_user.username, first_name=this_user.first_name, last_name=this_user.last_name,
            email=this_user.email, created_at=this_user.created_at, is_active=this_user.is_active, number_of_photos=this_user.number_of_photos if photo_count else 0
        )
    return user_profile


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


async def banned_user(user_id: int, current_user: User, db: Session):
    if current_user.user_role == UserRole.Admin.name:
        to_baned = db.query(User).filter(User.id == user_id).first()
        if to_baned:
            to_baned.is_active = False
            db.commit()
        return to_baned
    return PERMISSION_ERROR
