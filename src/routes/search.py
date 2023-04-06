from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.database.models import User, UserRole
from src.schemas import SearchModel, SearchResponse, UserModel
from src.services.auth import auth_service
from src.repository.search import get_search_posts, get_search_users
from src.services.roles import RoleChecker

router = APIRouter(prefix='/search', tags=['search'])


@router.post('/posts', response_model=List[SearchResponse], status_code=status.HTTP_200_OK)
async def search_posts(body: SearchModel, skip: int = 0, limit: int = 20,
                       current_user: User = Depends(auth_service.get_current_user),
                       db: Session = Depends(get_db)):
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
async def search_posts(body: SearchModel, skip: int = 0, limit: int = 20,
                       current_user: User = Depends(auth_service.get_current_user),
                       db: Session = Depends(get_db)):
    return await get_search_users(
        search_str=body.search_str,
        sort=body.sort,
        sort_type=body.sort_type,
        skip=skip,
        limit=limit,
        db=db)
