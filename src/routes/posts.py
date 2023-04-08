import uuid
import pathlib

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
async def create_post(body: PostCreate = Depends(), img_file: UploadFile = File(...), db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    # костиль для обхода проблеми коли на вхід всі теги ідуть однією строкою
    tags_list = []
    if len(body.tags) > 0:
        tags_list = body.tags[0].split(",")
        body.tags = tags_list

    if len(body.tags) > 5:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Too many tags. Available only 5 tags.")

    unique_filename = str(uuid.uuid4())+ pathlib.Path(img_file.filename).suffix
    file_path = f"media/{unique_filename}"
    with open(file_path, "wb") as f:
        f.write(await img_file.read())
    post = await posts_repository.create_post(body, file_path, db, current_user)
    return post


@router.get('/p/{post_id}', response_model=PostModel, status_code=status.HTTP_200_OK)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = await posts_repository.get_post(post_id, db)
    return post


@router.get('/u/{user_id}', response_model=List[PostModel], status_code=status.HTTP_200_OK)
async def get_user_posts(user_id: int, db: Session = Depends(get_db)):
    posts = await posts_repository.get_user_posts(user_id, db)
    return posts


@router.put('/p/{post_id}', response_model=PostModel, status_code=status.HTTP_200_OK)
async def update_post(post_id: int, body: PostCreate, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    if len(body.tags) > 5:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Too many tags. Available only 5 tags.")
    post = await posts_repository.update_post(post_id, body, db, current_user)
    return post


@router.delete('/p/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_post(post_id: int, db: Session = Depends(get_db)):
    post = await posts_repository.remove_post(post_id, db)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return post


@router.put('/d/{post_id}', status_code=status.HTTP_200_OK)
async def change_post_mark(post_id: int, db: Session = Depends(get_db)):
    post = await posts_repository.change_post_mark(post_id, db)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return post
