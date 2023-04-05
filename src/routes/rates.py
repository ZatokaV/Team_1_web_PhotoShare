from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List

from src.database.connect import get_db
from src.database.models import User, UserRole
from src.schemas import RateCreate, RateDB, RateResponse
from src.services.auth import auth_service
import src.repository.rates as rep_rates
from src.services.messages_templates import NOT_FOUND
from src.services.roles import RoleChecker

router = APIRouter(prefix='/rate', tags=['rate posts'])


@router.post('/{image_id}', response_model=RateDB, status_code=status.HTTP_201_CREATED)
async def set_rates_for_posts(image_id: int, body: RateCreate,
                              current_user: User = Depends(auth_service.get_current_user),
                              db: Session = Depends(get_db)):
    """
    The set_rates_for_posts function is used to set a rate for an image.
        The function takes in the following parameters:
            - image_id: int, which is the id of the image that will be rated.
            - body: RateCreate, which contains information about how to create a new rate object.
            - current_user: User = Depends(auth_service.get_current_user), which is used to get information about who
              created this post (the user). This parameter uses dependency injection and calls auth service's get
              current user function in order to retrieve this data from our database using SQLAlchemy OR

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
        It also takes in a current_user object and db session object as parameters, which are both optional.
        If no user is provided, then it will use auth_service to get one using Depends(auth_service.get_current_user).
        If no db session is provided, then it will use Depends(get_db) to create one.

    :param rate_id: int: Identify the rate to be removed
    :param current_user: User: Get the user who is currently logged in
    :param db: Session: Get a database session
    :return: The rate that was removed
    :doc-author: Trelent
    """
    rate = await rep_rates.remove_rate_for_image(rate_id, current_user, db)
    if rate is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=NOT_FOUND)


@router.get('/{image_id}', response_model=List[RateResponse], status_code=status.HTTP_200_OK)
async def get_rates_for_image(image_id: int, skip: int = 0, limit: int = 20,
                              current_user: User = Depends(auth_service.get_current_user),
                              db: Session = Depends(get_db)):
    """
    The get_rates_for_image function returns a list of rates for the image with the given id.
        The function takes in an optional skip and limit parameter to paginate through results.
        It also takes in a current_user object, which is used to determine if the user has already rated this image.

    :param image_id: int: Get the image id from the url
    :param skip: int: Skip a number of results
    :param limit: int: Limit the number of results returned
    :param current_user: User: Get the current user from the auth_service
    :param db: Session: Get the database session
    :return: A list of all the rates for an image
    """
    return await rep_rates.get_rate_for_image(image_id,  skip, limit, current_user, db)


@router.get('/', response_model=List[RateResponse], status_code=status.HTTP_200_OK)
async def get_rates_for_current_user(skip: int = 0, limit: int = 20,
                                     current_user: User = Depends(auth_service.get_current_user),
                                     db: Session = Depends(get_db)):
    """
    The get_rates_for_current_user function returns a list of rates for the current user.
        The function takes in three parameters: skip, limit, and current_user.
        Skip is an integer that determines how many items to skip before returning results.
        Limit is an integer that determines how many items to return after skipping the specified number of items.
        Current_user is a User object containing information about the currently logged-in user.

    :param skip: int: Skip the first n records
    :param limit: int: Limit the number of rates returned
    :param current_user: User: Get the current user
    :param db: Session: Connect to the database
    :return: The rates for the current user
    """
    return await rep_rates.get_rate_for_user(skip, limit, current_user, db)


@router.get('/user/{user_id}', response_model=List[RateResponse],
            dependencies=[Depends(RoleChecker([UserRole.Admin.name, UserRole.Moderator.name]))], status_code=status.HTTP_200_OK)
async def get_rate_from_user(user_id: int, skip: int = 0, limit: int = 20,
                             current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
    The get_rate_from_user function returns a list of all the ratings that a user has made.
        The function takes in an integer for the user_id, and two optional integers for skip and limit.
        It also takes in current_user as an object from auth_service, which is used to check if the
        requesting user is authorized to view this information. Finally, it takes in db as a Session object
        from get_db(), which allows us to access our database.

    :param user_id: int: Get the user id from the url
    :param skip: int: Skip the first n results
    :param limit: int: Limit the number of results returned
    :param current_user: User: Get the current user's info
    :param db: Session: Pass the database session to the function
    :return: A list of rates that the user has given to other users
    """
    return await rep_rates.get_rate_from_user(user_id, skip, limit, current_user, db)
