from datetime import datetime

from sqlalchemy.orm import Session

from src.database.models import User, Comment, Post
from src.schemas import CommentModel


async def create_comment(body: CommentModel, id_of_post: int, db: Session, current_user):
    """
    The create_comment function creates a new comment in the database.
        Args:
            body (CommentModel): The CommentModel object that contains the data for creating a new comment.
            id_of_post (int): The ID of the post to which this comment belongs.
            db (Session): A Session instance used to query and update our database.

    :param body: CommentModel: Get the comment_text from the user
    :param id_of_post: int: Identify the post that the comment is being added to
    :param db: Session: Access the database
    :param current_user: Get the user_id of the current user
    :return: A comment object
    :doc-author: Trelent
    """
    post = db.query(Post).filter_by(id=id_of_post).first()
    if not post:
        return None
    comment = Comment(
        comment_text=body.comment_text,
        post_id=id_of_post,
        user_id=current_user.id
    )
    db.add(comment)
    db.commit()
    return comment


async def get_comments(skip: int, limit: int, db: Session, id_of_post: int):
    """
    The get_comments function takes in a skip, limit, db and id_of_post.
    It then queries the database for all comments that have the same post_id as id_of_post.
    It then returns those comments.

    :param skip: int: Skip a certain amount of comments
    :param limit: int: Limit the number of comments returned
    :param db: Session: Pass the database session to the function
    :param id_of_post: int: Filter the comments by post_id
    :return: A list of comments
    :doc-author: Trelent
    """
    comments = db.query(Comment).filter_by(post_id=id_of_post).offset(skip).limit(limit).all()
    return comments


async def get_comment(db: Session, comment_id: int):
    """
    The get_comment function takes in a comment_id and returns the Comment object with that id.
        Args:
            db (Session): The database session to use for querying.
            comment_id (int): The id of the Comment to retrieve from the database.

    :param db: Session: Pass the database session to the function
    :param comment_id: int: Filter the query to return only a single comment
    :return: The comment object with the given id
    :doc-author: Trelent
    """
    comment = db.query(Comment).filter_by(id=comment_id).first()
    return comment


async def get_user_by_comment_id(db: Session, user_id: int):
    """
    The get_user_by_comment_id function takes in a database session and a user_id,
    and returns the User object associated with that id. If no such user exists, it returns None.

    :param db: Session: Pass the database session to the function
    :param user_id: int: Filter the user by id
    :return: The user associated with the comment
    :doc-author: Trelent
    """
    user = db.query(User).filter_by(id=user_id).first()
    return user


async def edit_comments(comment_id: int, body: CommentModel, db: Session, current_user: User):
    """
    The edit_comments function takes in a comment_id, body, db and current_user.
    It then queries the database for a comment with the given id and user id. If it finds one,
    it updates that comments text to be equal to what was passed in as body.comment_text
    and sets its updated at time to now.

    :param comment_id: int: Identify the comment to be deleted
    :param body: CommentModel: Pass the data from the request body to the function
    :param db: Session: Access the database
    :param current_user: User: Check if the user is authorized to edit the comment
    :return: The comment that was edited
    :doc-author: Trelent
    """
    comment = db.query(Comment).filter_by(id=comment_id, user_id=current_user.id).first()
    if comment:
        comment.comment_text = body.comment_text
        comment.updated_at = datetime.now()
        db.commit()
    return comment


async def delete_comments(comment_id: int, db: Session):
    """
    The delete_comments function deletes a comment from the database.
        Args:
            comment_id (int): The id of the comment to be deleted.
            current_user (User): The user who is deleting the comment.
            db (Session): A session object for interacting with our database.

    :param comment_id: int: Identify the comment that is to be deleted
    :param db: Session: Pass in the database session
    :return: A none type
    :doc-author: Trelent
    """
    comment = db.query(Comment).filter_by(id=comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()