from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import src.repository.users as repository_users
from src.database.connect import get_db
from src.database.models import User
from src.schemas import UserModel, UserProfileModel, UserBase, UserUpdate
from src.services.auth import auth_service
from src.services.messages_templates import NOT_FOUND, NOT_FOUND_OR_DENIED

router = APIRouter(prefix='/users', tags=["users"])


@router.get('/all', response_model=List[UserModel])
async def get_contacts(db: Session = Depends(get_db)):
    all_users = await repository_users.get_all_users(User(id=1), db)
    if all_users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
    return all_users


@router.get("/get_user_profile", response_model=UserProfileModel)
async def get_user_profile(username: str, db: Session = Depends(get_db)):
    user_profile = await repository_users.get_user_profile(username, db)
    if user_profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
    return user_profile


@router.put("/update_user_self", response_model=UserModel)
async def update_user_self(
        body: UserBase,
        user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)):
    user = await repository_users.update_user_self(body, user, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
    return user


@router.put("/update_user_as_admin", response_model=UserModel)
async def update_user_as_admin(
        body: UserUpdate,
        user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)):
    user = await repository_users.update_user_as_admin(body, user, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND_OR_DENIED)
    return user


@router.put("/banned_user", response_model=UserProfileModel)
async def banned_user(user_id: int, current_user: User = Depends(auth_service.get_current_user),
                      db: Session = Depends(get_db)):
    banned = await repository_users.banned_user(user_id, current_user, db)
    if banned is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
    return banned
