from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.sql import extract

from src.database.models import Post, User, Tag
from src.schemas import TagBase, TagModel


def get_tag_by_name(tag_name: str, db:Session) -> Tag | None:
    tag = db.query(Tag).filter(Tag.tag == tag_name.tag).first()
    return tag


def create_tag(tag_name: str, user, db: Session):
    tag = Tag(tag=tag_name.tag, user_id=user.id)
    db.add(tag)
    db.commit()
    db.refresh(tag)

    return tag
