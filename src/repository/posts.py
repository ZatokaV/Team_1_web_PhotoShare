from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.sql import extract

from src.database.models import Post, User, Tag
from src.schemas import PostBase, PostModel, PostCreate
from src.repository import tags as repository_tags


async def create_post(body: PostCreate, file_path: str, db: Session, user: User) -> Post:
    tags_list = repository_tags.get_tags_list(body.tags, user, db)

    post = Post(photo_url=file_path, description=body.description, user_id=user.id, tags=tags_list)
    db.add(post)
    db.commit()
    db.refresh(post)

    return post


async def get_post(post_id: int, db: Session) -> Post:
    post = db.query(Post).filter(Post.id == post_id).first()
    return post


async def get_user_posts(user_id: int, db: Session) -> List[Post]:
    posts = db.query(Post).filter(Post.user_id == user_id).all()
    return posts


async def remove_post(post_id: int, db: Session):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
    return post


async def update_post(post_id: int, body, db: Session, user) -> Post | None:
    post = db.query(Post).filter(Post.id == post_id).first()

    if post:
        tags_list = repository_tags.get_tags_list(body.tags, user, db)

        post.description = body.description
        post.tags = tags_list
        db.commit()
        db.refresh(post)
    return post


async def change_post_mark(post_id: int, db: Session) -> Post | None:
    post = db.query(Post).filter(Post.id == post_id).first()

    if post:
        post.marked = not post.marked
        db.commit()
        db.refresh(post)
    return post
