from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import src.repository.users as repository_users
from src.database.connect import get_db
from src.database.models import User
from src.schemas import UserModel, UserProfileModel
from src.services.messages_templates import NOT_FOUND

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
