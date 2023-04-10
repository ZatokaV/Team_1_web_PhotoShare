from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.sql import extract

from src.database.models import Post, User, Tag
from src.schemas import PostBase, PostModel, PostCreate
from src.repository import tags as repository_tags


async def create_post(body: PostCreate, file_path: str, db: Session, user: User) -> Post:
    """
    Add new post

    :param body: Data for create new post
    :type body: PostCreate
    :param file_path: Path to file
    :type file_path: str
    :param db: Database session
    :type db: Session
    :param user: User.
    :type user: User
    :return: Added post
    :rtype: Post
    """

    tags_list = repository_tags.get_tags_list(body.tags, user, db)

    post = Post(photo_url=file_path, description=body.description, user_id=user.id, tags=tags_list)
    db.add(post)
    db.commit()
    db.refresh(post)

    return post


async def get_post(post_id: int, db: Session) -> Post:
    """
    Get post by ID

    :param post_id: Post's ID
    :type post_id: int
    :param db: Database session
    :type db: Session
    :return: Return post by ID
    :rtype: Post
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    return post


async def get_user_posts(user_id: int, db: Session) -> List[Post]:
    """
    Get all user's posts

    :param user_id: User's ID
    :type user_id: int
    :param db: Database session
    :type db: Session
    :return: Get all user's posts
    :rtype: List[Post]
    """

    posts = db.query(Post).filter(Post.user_id == user_id).all()
    return posts


async def remove_post(post_id: int, db: Session):
    """
    Remove post by ID

    :param post_id: Post's ID
    :type post_id: int
    :param db: Database session
    :type db: Session
    """

    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
    return post


async def update_post(post_id: int, body: PostCreate, db: Session, user: User) -> Post | None:
    """
    Update description and tags

    :param post_id: Post's ID
    :type post_id: int
    :param body: Data for update post
    :type body: PostCreate
    :param db: Database session
    :type db: Session
    :param user: User.
    :type user: User
    :return: Updated post
    :rtype: Post | None
    """

    post = db.query(Post).filter(Post.id == post_id).first()

    if post:
        tags_list = repository_tags.get_tags_list(body.tags, user, db)

        post.description = body.description
        post.tags = tags_list
        db.commit()
        db.refresh(post)
    return post


async def change_post_mark(post_id: int, db: Session) -> Post | None:
    """
    Change soft-delete mark for post

    :param post_id: Post's ID
    :type post_id: int
    :param db: Database session
    :type db: Session
    :return: Post
    :rtype: Post | None
    """

    post = db.query(Post).filter(Post.id == post_id).first()

    if post:
        post.marked = not post.marked
        db.commit()
        db.refresh(post)
    return post
