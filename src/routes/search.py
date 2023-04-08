from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.database.models import User, UserRole
from src.schemas import SearchModel, SearchResponse, UserModel, SearchUserModel
from src.services.auth import auth_service
from src.repository.search import get_search_posts, get_search_users
from src.services.roles import RoleChecker

router = APIRouter(prefix='/search', tags=['search'])


@router.post('/posts', response_model=List[SearchResponse], status_code=status.HTTP_200_OK)
async def search_posts(body: SearchModel, skip: int = 0, limit: int = 20,
                       current_user: User = Depends(auth_service.get_current_user),
                       db: Session = Depends(get_db)):
    """
    The search_posts function is used to search for posts based on a string.
    The function takes in the following parameters:
        - body: The SearchModel object containing the search_str, sort, and sort_type fields.
        - skip (optional): The number of posts to skip before returning results. Default value is 0.
        - limit (optional): The maximum number of posts to return per request. Default value is 20.

    :param body: SearchModel: Get the search string from the request body
    :param skip: int: Skip the first n posts
    :param limit: int: Limit the number of posts returned
    :param current_user: User: Get the current user
    :param db: Session: Pass the database session to the function
    :return: A list of posts
    :doc-author: Trelent
    """
    return await get_search_posts(
        search_str=body.search_str,
        sort=body.sort,
        sort_type=body.sort_type,
        skip=skip,
        limit=limit,
        db=db)


@router.post('/users', response_model=List[UserModel],
             dependencies=[Depends(RoleChecker([UserRole.Admin.name, UserRole.Moderator.name]))],
             status_code=status.HTTP_200_OK)
async def search_posts(body: SearchUserModel, skip: int = 0, limit: int = 20,
                       current_user: User = Depends(auth_service.get_current_user),
                       db: Session = Depends(get_db)):
    """
    The search_posts function is used to search for users based on a string.
    The function takes in the following parameters:
        - body: The SearchUserModel object containing the search_str, sort, and sort_type fields.
        - skip (optional): The number of posts to skip before returning results. Defaults to 0 if not specified.
        - limit (optional): The maximum number of posts that can be returned at once. Defaults to 20 if not specified.

    :param body: SearchUserModel: Get the search string from the request body
    :param skip: int: Skip a number of posts in the database
    :param limit: int: Limit the number of results returned
    :param current_user: User: Get the current user
    :param db: Session: Access the database
    :return: A list of posts
    :doc-author: Trelent
    """
    return await get_search_users(
        search_str=body.search_str,
        sort=body.sort,
        sort_type=body.sort_type,
        skip=skip,
        limit=limit,
        db=db)
