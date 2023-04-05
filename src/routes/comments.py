from typing import List

from fastapi import Path, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.database.models import User
from src.schemas import CommentModel, CommentBase, CommentResponse
import src.repository.comments as comment_repository
from src.services.auth import auth_service

router = APIRouter(prefix="/{post_id}/comments", tags=["comments"])


@router.post("/add_comment", status_code=status.HTTP_201_CREATED, response_model=CommentBase)
async def add_comments(body: CommentModel, post_id: int = Path(ge=1),
                       db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    comment = await comment_repository.create_comment(body, post_id, db, current_user)
    return comment


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[CommentResponse])
async def get_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), post_id: int = Path(ge=1)):
    comment_user = []
    comments = await comment_repository.get_comments(skip, limit, db, post_id)
    if comments:
        for comment_model in comments:
            user_model = await comment_repository.get_user_by_comment_id(db, comment_model.user_id)
            response = CommentResponse(comment=comment_model,
                                       user_first_name=user_model.first_name,
                                       user_last_name=user_model.last_name,
                                       username=user_model.username,
                                       user_avatar=None
                                       )
            comment_user.append(response)
    return comment_user


@router.get("/{comment_id}", status_code=status.HTTP_200_OK, response_model=CommentResponse)
async def get_comment(db: Session = Depends(get_db), comment_id: int = Path(ge=1)):
    comment_model = await comment_repository.get_comment(db, comment_id)
    if comment_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    user_model = await comment_repository.get_user_by_comment_id(db, comment_model.user_id)

    comment_response = CommentResponse(comment=comment_model,
                                       user_first_name=user_model.first_name,
                                       user_last_name=user_model.last_name,
                                       username=user_model.username,
                                       user_avata=None
                                       )

    return comment_response


@router.patch("/{comment_id}/edit_comment", status_code=status.HTTP_200_OK, response_model=CommentBase)
async def edit_comment(body: CommentModel, comment_id: int = Path(ge=1), db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    comment = await comment_repository.edit_comments(comment_id, body, db, current_user)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(comment_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    await comment_repository.delete_comments(comment_id, current_user, db)
