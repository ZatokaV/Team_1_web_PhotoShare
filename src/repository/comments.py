from datetime import datetime

from sqlalchemy.orm import Session

from src.database.models import User, Comment
from src.schemas import CommentModel


async def create_comment(body: CommentModel, id_of_post: int, db: Session, current_user):
    comment = Comment(
        comment_text=body.comment_text,
        post_id=id_of_post,
        user_id=current_user.id
    )
    db.add(comment)
    db.commit()
    return comment


async def get_comments(skip: int, limit: int, db: Session, id_of_post: int):
    comments = db.query(Comment).filter_by(post_id=id_of_post).offset(skip).limit(limit).all()
    return comments


async def get_comment(db: Session, comment_id: int):
    comment = db.query(Comment).filter_by(id=comment_id).first()
    return comment


async def get_user_by_comment_id(db: Session, user_id: int):
    user = db.query(User).filter_by(id=user_id).first()
    return user


async def edit_comments(comment_id: int, body: CommentModel, db: Session, current_user: User):
    comment = db.query(Comment).filter_by(id=comment_id, user_id=current_user.id).first()
    if comment:
        comment.comment_text = body.comment_text
        comment.updated_at = datetime.now()
        db.commit()
    return comment


async def delete_comments(comment_id: int, current_user: User, db: Session):
    comment = db.query(Comment).filter_by(id=comment_id, user_id=current_user.id).first()
    if comment:
        db.delete(comment)
        db.commit()