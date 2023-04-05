from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.sql import extract

from src.database.models import Post, User, Tag
from src.schemas import PostBase, PostModel, PostCreate
from src.repository import tags as repository_tags


async def create_post(body: PostCreate, db: Session, user: User) -> Post:
    tags = body.tags
    tagslist = []
    for tag_name in tags:
        tag = repository_tags.get_tag_by_name(tag_name, db)
        if not tag:
            tag = repository_tags.create_tag(tag_name, user, db)
        tagslist.append(tag)

    post = Post(photo_url=body.photo_url, description=body.description, user_id=user.id, tags=tagslist)
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
