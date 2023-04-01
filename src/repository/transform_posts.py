from sqlalchemy.orm import Session
from typing import List

from src.database.models import TransformPosts, Post


async def get_image_for_transform(image_id: int, db: Session) -> str | None:
    image = db.query(Post).filter(Post.id == image_id).first()
    image_path = None
    if image:
        image_path = image.photo_url
    return image_path


async def set_transform_image(image_id: int, modify_url: str, db: Session) -> TransformPosts | None:
    # image = db.query(Post).filter(Post.id == image_id).first()
    image = TransformPosts(photo_url=modify_url, photo_id=image_id)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


async def get_transform_image(image_id: int, db: Session) -> TransformPosts | None:
    return db.query(TransformPosts).filter(TransformPosts.id == image_id).first()


async def get_all_transform_images(image_id: int, db: Session) -> List[TransformPosts]:
    return db.query(TransformPosts).filter(TransformPosts.photo_id == image_id).all()
