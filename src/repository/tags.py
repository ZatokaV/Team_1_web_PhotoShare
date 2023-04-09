from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.sql import extract

from src.database.models import Post, User, Tag
from src.schemas import TagBase, TagModel


def get_tag_by_name(tag_name: str, db: Session) -> Tag | None:
    tag = db.query(Tag).filter(Tag.tag == tag_name).first()
    return tag


def create_tag(tag_name: str, user, db: Session):
    tag = Tag(tag=tag_name, user_id=user.id)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def get_tags_list(tags: list, user, db: Session) -> List[Tag]:
    tags_list = []
    if len(tags) > 0:
        for tag_name in tags:
            tag = get_tag_by_name(tag_name, db)
            if not tag:
                tag = create_tag(tag_name, user, db)
            tags_list.append(tag)

    return tags_list
