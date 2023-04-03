from datetime import datetime
from typing import List
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import User, RatePost, UserRole, Post
from src.schemas import RateResponse


async def set_rate_for_image(image_id: int, user_rate: int, current_user: User, db: Session) -> RatePost:
    """
    The set_rate_for_image function is used to set a rate for an image.
        The function takes in the following parameters:
            - image_id: int, the id of the image that will be rated.
            - body: RateCreate, contains information about how to rate an image (rate).
            - current_user: User, contains information about who is rating this photo (user_id).

    :param image_id: int: Identify the image that is being rated
    :param body: RateCreate: Get the rate value from the request body
    :param current_user: User: Get the current user that is logged in
    :param db: Session: Access the database
    :return: A rate object
    """
    post = db.query(Post).filter(and_(Post.id == image_id, Post.user_id != current_user.id)).first()
    rate = None
    if post:
        rate = db.query(RatePost).filter(and_(RatePost.photo_id == image_id,
                                              RatePost.user_id == current_user.id)).first()
        if rate is None:
            rate = RatePost(photo_id=image_id, user_id=current_user.id, rate=user_rate)
            db.add(rate)
        else:
            rate.rate = user_rate
            rate.updated_at = datetime.now()
        db.commit()
        db.refresh(rate)
    return rate


async def remove_rate_for_image(rate_id: int, current_user: User, db: Session) -> None:
    """
    The remove_rate_for_image function removes a rate for an image.
        Args:
            rate_id (int): The id of the rate to be removed.
            current_user (User): The user who is making the request.
            db (Session): A database session object used to query and update data in the database.

    :param rate_id: int: Identify the rate that is to be removed
    :param current_user: User: Check if the user is an admin or not
    :param db: Session: Access the database
    :return: None
    """
    if current_user.user_role == UserRole.User.name:
        rate = db.query(RatePost).filter(and_(RatePost.id == rate_id, RatePost.user_id == current_user.id)).first()
    else:
        rate = db.query(RatePost).filter(RatePost.id == rate_id).first()
    if rate:
        db.delete(rate)
        db.commit()
    return rate


async def get_rate_for_image(image_id: int, current_user: User, db: Session) -> List[RateResponse]:
    """
    The get_rate_for_image function is used to get the rate for a specific image. The function takes in an image_id,
    current_user and db as parameters. If the user role of the current user is User, then it will query RatePost,
    User and Post tables using join() method to filter out all rows where post id matches with given image id and
    post's user id matches with current users' ID. It will return only one row from database which satisfies these
    conditions.

    :param image_id: int: Get the image id from the database
    :param current_user: User: Get the current user's information
    :param db: Session: Access the database
    :return: The rate of the image
    """
    if current_user.user_role == UserRole.User.name:
        rates = db.query(RatePost.id, RatePost.rate, RatePost.user_id, User.username, RatePost.photo_id, Post.photo_url,
                         RatePost.created_at, RatePost.updated_at).select_from(Post).join(RatePost).join(User).filter(
            and_(Post.id == image_id, Post.user_id == current_user.id)).all()
    else:
        rates = db.query(RatePost.id, RatePost.rate, RatePost.user_id, User.username, RatePost.photo_id, Post.photo_url,
                         RatePost.created_at, RatePost.updated_at).select_from(Post).join(RatePost).join(User).filter(
            RatePost.photo_id == image_id).all()
    return rates


async def get_rate_for_user(current_user: User, db: Session) -> List[RateResponse]:
    """
    The get_rate_for_user function takes in a current_user and db object, and returns a list of RateResponse objects.
    The function queries the database for all rate posts that have been created by the user with id equal to current_user.id.

    :param current_user: User: Get the current user from the database
    :param db: Session: Access the database
    :return: A list of rateresponse objects
    """
    rates = db.query(RatePost.id, RatePost.rate, RatePost.user_id, User.username, RatePost.photo_id, Post.photo_url,
                     RatePost.created_at, RatePost.updated_at).select_from(Post).join(RatePost).join(User).filter(
                     RatePost.user_id == current_user.id).all()
    return rates


async def get_rate_from_user(user_id: int, current_user: User, db: Session) -> List[RateResponse]:
    """
    The get_rate_from_user function takes in a user_id, current_user, and db.
    It returns a list of RateResponse objects that contain the rate information for the given user.

    :param user_id: int: Identify the user who is currently logged in
    :param current_user: User: Get the user id of the current logged in user
    :param db: Session: Access the database
    :return: A list of rateresponse objects
    """
    rates = []
    if current_user.user_role != UserRole.User.name:
        rates = db.query(RatePost.id, RatePost.rate, RatePost.user_id, User.username, RatePost.photo_id, Post.photo_url,
                         RatePost.created_at, RatePost.updated_at).select_from(Post).join(RatePost).join(User).filter(
            RatePost.user_id == user_id).all()
    return rates
