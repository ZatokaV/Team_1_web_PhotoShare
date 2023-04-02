from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List

from src.database.connect import get_db
from src.database.models import User
from src.schemas import RateCreate, RateDB, RateResponse
from src.services.auth import auth_service
import src.repository.rates as rep_rates
from src.services.messages_templates import NOT_FOUND

router = APIRouter(prefix='/rate', tags=['rate posts'])


@router.post('/{image_id}', response_model=RateDB, status_code=status.HTTP_200_OK)
async def set_rates_for_posts(image_id: int, body: RateCreate,
                              current_user: User = Depends(auth_service.get_current_user),
                              db: Session = Depends(get_db)):
    """
    The set_rates_for_posts function is used to set a rate for an image.
        The function takes in the following parameters:
            - image_id: int, which is the id of the image that will be rated.
            - body: RateCreate, which contains information about how to create a new rate object.
            - current_user: User = Depends(auth_service.get_current_user), which is used to get information about who created this post (the user). This parameter uses dependency injection and calls auth service's get current user function in order to retrieve this data from our database using SQLAlchemy OR

    :param image_id: int: Identify the image that is being rated
    :param body: RateCreate: Get the rate value from the request body
    :param current_user: User: Get the current user from the database
    :param db: Session: Get the database session
    :return: The rate object that was created
    """
    rate = await rep_rates.set_rate_for_image(image_id, body.rate, current_user, db)
    if rate is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=NOT_FOUND)
    return rate


@router.delete('/{rate_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_rate(rate_id: int, current_user: User = Depends(auth_service.get_current_user),
                              db: Session = Depends(get_db)):
    """
    The remove_rate function is used to remove a rate from the database.
        The function takes in an integer, which represents the id of the rate that will be removed.
        It also takes in a current_user object and db session object as parameters, but these are not required by default.

    :param rate_id: int: Identify the rate to be removed
    :param current_user: User: Get the current user
    :param db: Session: Get the database session
    :return: The rate that was removed from the database
    :doc-author: Trelent
    """
    rate = await rep_rates.remove_rate_for_image(rate_id, current_user, db)
    if rate is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=NOT_FOUND)


@router.get('/{image_id}', response_model=List[RateResponse], status_code=status.HTTP_200_OK)
async def get_rates_for_image(image_id: int, current_user: User = Depends(auth_service.get_current_user),
                              db: Session = Depends(get_db)):
    """
    The get_rates_for_image function is used to get the rates for a specific image.
        The function takes in an image_id and returns a list of all the rates for that image.

    :param image_id: int: Get the image id from the url
    :param current_user: User: Get the current user from the database
    :param db: Session: Get the database session
    :return: The rate of an image for the current user
    :doc-author: Trelent
    """
    return await rep_rates.get_rate_for_image(image_id, current_user, db)


@router.get('/', response_model=List[RateResponse], status_code=status.HTTP_200_OK)
async def get_rates_for_current_user(current_user: User = Depends(auth_service.get_current_user),
                                     db: Session = Depends(get_db)):
    """
    The get_rates_for_current_user function returns the rates for the current user.
        The function takes in a User object and a Session object as parameters,
        which are provided by Depends() functions. The get_rates_for_current_user function then calls
        rep-rates' get_rate_for user method to return the rates for that particular user.

    :param current_user: User: Get the current user that is logged in
    :param db: Session: Get the database session
    :return: A list of rates for the current user
    :doc-author: Trelent
    """
    return await rep_rates.get_rate_for_user(current_user, db)


@router.get('/user/{user_id}', response_model=List[RateResponse], status_code=status.HTTP_200_OK)
async def get_rate_from_user(user_id: int, current_user: User = Depends(auth_service.get_current_user),
                                     db: Session = Depends(get_db)):
    """
    The get_rate_from_user function returns the rate of a user from another user.
        The function takes in an integer representing the id of the target user, and two optional parameters:
            - current_user: A User object representing the currently logged-in user. This is used to determine which
                            rate to return (if any). If no such rate exists, None is returned instead. Defaults to None.
            - db: A Session object that represents a database session for querying data from our database using SQLAlchemy's ORM model.

    :param user_id: int: Get the user id from the request body
    :param current_user: User: Get the user that is currently logged in
    :param db: Session: Connect to the database
    :return: The rate of a user by the current user
    :doc-author: Trelent
    """
    return await rep_rates.get_rate_from_user(user_id, current_user, db)

