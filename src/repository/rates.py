from datetime import datetime
from typing import List
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import User, RatePost, UserRole, Post
from src.schemas import RateResponse


async def set_rate_for_image(image_id: int, user_rate: int, current_user: User, db: Session) -> RatePost:
    """
    The set_rate_for_image function takes in an image_id, a user_rate, the current user and a database session. It
    then queries the Post table for any posts that match the given image id and are not posted by the current user.
    If there is such a post it will query for any rates on that post by this particular user. If there is no rate
    yet, it will create one with this users rating of said photo. Otherwise it updates their previous rating to
    reflect their new one.

    :param image_id: int: Identify the image that we want to rate
    :param user_rate: int: Set the rate of the image
    :param current_user: User: Get the id of the user who is currently logged in
    :param db: Session: Access the database
    :return: A ratepost object
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


async def get_rate_for_image(image_id: int, skip: int, limit: int, current_user: User,
                             db: Session) -> List[RateResponse]:
    """
    The get_rate_for_image function returns a list of rates for the image with the given id.
        If current_user is an admin, all rates are returned. Otherwise, only those created by current_user are returned.

    :param image_id: int: Filter the rate_posts table by image id
    :param skip: int: Skip the first n rows in a result set before beginning to return rows
    :param limit: int: Limit the number of results returned
    :param current_user: User: Check if the user is an admin or not
    :param db: Session: Access the database
    :return: The list of rates for the image with the given id
    """
    if current_user.user_role == UserRole.User.name:
        rates = db.query(RatePost.id, RatePost.rate, RatePost.user_id, User.username, RatePost.photo_id, Post.photo_url,
                         RatePost.created_at, RatePost.updated_at).select_from(Post).join(RatePost).join(User).filter(
            and_(Post.id == image_id, Post.user_id == current_user.id)).offset(skip).limit(limit).all()
    else:
        rates = db.query(RatePost.id, RatePost.rate, RatePost.user_id, User.username, RatePost.photo_id, Post.photo_url,
                         RatePost.created_at, RatePost.updated_at).select_from(Post).join(RatePost).join(User).filter(
            RatePost.photo_id == image_id).offset(skip).limit(limit).all()
    return rates


async def get_rate_for_user(skip: int, limit: int, current_user: User, db: Session) -> List[RateResponse]:
    """
    The get_rate_for_user function returns a list of rate objects for the current user. Args: skip (int): The number
    of items to skip before starting to collect the result set. limit (int): The numbers of items to return after
    skipping &quot;skip&quot; elements. current_user (User): A User object representing the currently logged in user,
    used for authorization purposes.  This is passed from FastAPI's dependency injection system and should not be
    manually created by users of this function!  See
    https://fastapi.tiangolo.com/advanced/dependencies/#injecting-security-sc

    :param skip: int: Skip the first n records in the query
    :param limit: int: Limit the number of results returned
    :param current_user: User: Get the current user from the database
    :param db: Session: Access the database
    :return: A list of rate responses
    """
    rates = db.query(RatePost.id, RatePost.rate, RatePost.user_id, User.username, RatePost.photo_id, Post.photo_url,
                     RatePost.created_at, RatePost.updated_at).select_from(Post).join(RatePost).join(User).filter(
                     RatePost.user_id == current_user.id).offset(skip).limit(limit).all()
    return rates


async def get_rate_from_user(user_id: int, skip: int, limit: int, current_user: User,
                             db: Session) -> List[RateResponse]:
    """
    The get_rate_from_user function takes in a user_id, skip, limit, current_user and db. It returns a list of
    RateResponse objects. If the current user is not an admin or moderator then it will query the database for all
    rates that have been made by the specified user id and return them as RateResponse objects.

    :param user_id: int: Get the user id of the user who is logged in
    :param skip: int: Skip the first n records
    :param limit: int: Limit the number of results returned
    :param current_user: User: Check if the user is an admin or not
    :param db: Session: Access the database
    :return: The rate of a user
    """
    rates = []
    if current_user.user_role != UserRole.User.name:
        rates = db.query(RatePost.id, RatePost.rate, RatePost.user_id, User.username, RatePost.photo_id, Post.photo_url,
                         RatePost.created_at, RatePost.updated_at).select_from(Post).join(RatePost).join(User).filter(
            RatePost.user_id == user_id).offset(skip).limit(limit).all()
    return rates
