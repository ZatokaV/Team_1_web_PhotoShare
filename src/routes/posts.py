from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query, File, UploadFile, Form
from fastapi_limiter.depends import RateLimiter
from fastapi_limiter import FastAPILimiter
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.database.models import User, Post
from src.services.auth import auth_service
from src.schemas import PostBase, PostModel, PostCreate
from src.repository import posts as posts_repository


router = APIRouter(prefix='/posts', tags=['posts'])


@router.post('/p', response_model=PostModel, status_code=status.HTTP_201_CREATED)
async def create_post(body: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    post = await posts_repository.create_post(body, db, current_user)
    return post


@router.get('/p/{post_id}', response_model=PostModel, status_code=status.HTTP_200_OK)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = await posts_repository.get_post(post_id, db)
    return post


@router.get('/u/{user_id}', response_model=List[PostModel], status_code=status.HTTP_200_OK)
async def get_user_posts(user_id: int, db: Session = Depends(get_db)):
    posts = await posts_repository.get_user_posts(user_id, db)
    return posts


# @router.put('/p/{post_id}', status_code=status.HTTP_200_OK)
# async def update_post(post_id: int, body, db: Session):
    # pass
