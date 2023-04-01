from sqlalchemy import and_
from sqlalchemy.orm import Session
from typing import List

from src.database.models import TransformPosts, Post, User, UserRole


async def get_image_for_transform(image_id: int, current_user: User, db: Session) -> str | None:
    if current_user.user_role == UserRole.Admin.name:
        image = db.query(Post).filter(Post.id == image_id).first()
    else:
        image = db.query(Post).filter(and_(Post.id == image_id, Post.user_id == current_user.id)).first()
    image_path = None
    if image:
        image_path = image.photo_url
    return image_path


async def set_transform_image(image_id: int, modify_url: str, current_user: User, db: Session) -> TransformPosts | None:
    image = None
    if current_user.user_role == UserRole.Admin.name:
        photo = db.query(Post).filter(Post.id == image_id).first()
    else:
        photo = db.query(Post).filter(and_(Post.id == image_id, Post.user_id == current_user.id)).first()
    if photo:
        image = TransformPosts(photo_url=modify_url, photo_id=photo.id)
        db.add(image)
        db.commit()
        db.refresh(image)
    return image


async def get_transform_image(image_id: int, current_user: User, db: Session) -> TransformPosts | None:
    if current_user.user_role == UserRole.Admin.name:
        img = db.query(TransformPosts).filter(TransformPosts.id == image_id).first()
    else:
        img = db.query(TransformPosts).join(Post).filter(and_(TransformPosts.id == image_id,
                                                              Post.user_id == current_user.id)).first()
    return img


async def remove_transform_image(image_id: int, current_user: User, db: Session) -> TransformPosts | None:
    if current_user.user_role == UserRole.Admin.name:
        img = db.query(TransformPosts).filter(TransformPosts.id == image_id).first()
    else:
        img = db.query(TransformPosts).join(Post).filter(and_(Post.id == image_id,
                                                              Post.user_id == current_user.id)).first()
    if img:
        db.delete(img)
        db.commit()
    return img


async def get_all_transform_images(image_id: int, current_user: User, db: Session) -> List[TransformPosts]:
    if current_user.user_role == UserRole.Admin.name:
        list_image = db.query(TransformPosts).filter(TransformPosts.photo_id == image_id).all()
    else:
        list_image = db.query(TransformPosts).join(Post).filter(and_(Post.id == image_id,
                                                                     Post.user_id == current_user.id)).all()
    return list_image


async def get_all_transform_images_for_user(current_user: User, db: Session) -> List[TransformPosts]:
    if current_user.user_role == UserRole.Admin.name:
        list_image = db.query(TransformPosts).all()
    else:
        list_image = db.query(TransformPosts).join(Post).filter(Post.user_id == current_user.id).all()
    return list_image
