from sqlalchemy import and_
from sqlalchemy.orm import Session
from datetime import datetime

from src.database.models import User, Post, UserRole
from src.schemas import UserModel, UserProfileModel, UserBase, UserUpdate
from src.services.messages_templates import PERMISSION_ERROR


async def create_user(body: UserModel, db: Session) -> User:
    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_user_self(body: UserBase, user: User, db: Session) -> User | None:
    user = db.query(User).filter(User.id == user.id).first()
    if user:
        user.username = body.username
        user.first_name = body.first_name
        user.last_name = body.last_name
        user.email = body.email
        user.updated_at = datetime.now().isoformat()
        db.commit()
    return user


async def update_user_as_admin(body: UserUpdate, user: User, db: Session) -> User | None:
    user_to_update = db.query(User).filter(User.username == body.username).first()
    if user_to_update:
        if user.user_role == UserRole.Admin.name:
            user_to_update.username = body.username
            user_to_update.first_name = body.first_name
            user_to_update.last_name = body.last_name
            user_to_update.email = body.email
            user_to_update.is_active = body.is_active
            user_to_update.user_role = body.user_role
            user_to_update.updated_at = datetime.now().isoformat()
            db.commit()
        return user_to_update
    return None


async def get_user_profile(username: str, db: Session) -> UserProfileModel | None:
    this_user = db.query(User).filter(User.username == username).first()
    user_profile = None    
    if this_user:
        photo_count = db.query(Post).filter(Post.user_id == this_user.id).count()
        photo_count = 0 if not photo_count else photo_count
        user_profile = UserProfileModel(
            id=this_user.id, username=this_user.username, first_name=this_user.first_name,
            last_name=this_user.last_name,
            email=this_user.email, created_at=this_user.created_at, is_active=this_user.is_active,
            number_of_photos=photo_count
        )
    return user_profile


async def get_user_by_email(email: str, db: Session) -> User | None:
    return db.query(User).filter(User.email == email).first()


async def get_all_users(user: User, db: Session):
    all_users = db.query(User).filter(and_(user.id == 1)).all()
    return all_users


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


# async def banned_user(user_id: int, db: Session):
#     to_baned = db.query(User).filter(User.id == user_id).first()
#     if to_baned:
#         to_baned.is_active = False
#         db.commit()
#     return to_baned
