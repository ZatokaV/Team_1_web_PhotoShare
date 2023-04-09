from typing import List

from fastapi import Path, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.database.models import User, UserRole
from src.schemas import CommentModel, CommentBase, CommentResponse
import src.repository.comments as comment_repository
from src.services.auth import auth_service
from src.services.roles import RoleChecker

router = APIRouter(prefix="/{post_id}/comments", tags=["comments"])


@router.post("/add_comment", status_code=status.HTTP_201_CREATED, response_model=CommentBase)
async def add_comments(body: CommentModel, post_id: int = Path(ge=1),
                       db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The add_comments function creates a new comment for the post with the given id.
    The function takes in a CommentModel object, which is validated by Pydantic and then passed to the create_comment method of our repository.
    If no post with that ID exists, we raise an HTTPException indicating that there was no such resource found.

    :param body: CommentModel: Get the data from the request body
    :param post_id: int: Get the post id from the path
    :param db: Session: Get the database session
    :param current_user: User: Get the user that is currently logged in
    :return: A commentmodel object, which is a pydantic model
    :doc-author: Trelent
    """
    comment = await comment_repository.create_comment(body, post_id, db, current_user)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return comment


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[CommentResponse])
async def get_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), post_id: int = Path(ge=1)):
    """
    The get_comments function returns a list of comments for the specified post.
        The function takes in three parameters: skip, limit, and post_id.
        Skip is used to specify how many comments to skip before returning results (defaults to 0).
        Limit is used to specify how many results should be returned (defaults to 100).


    :param skip: int: Skip the first n comments
    :param limit: int: Limit the number of comments returned
    :param db: Session: Get the database session
    :param post_id: int: Get the comments for a specific post
    :return: A list of commentresponse objects
    :doc-author: Trelent
    """
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
    """
    The get_comment function returns a CommentResponse object containing the comment, user_first_name,
    user_last_name and username of the comment with id = comment_id. If no such comment exists in the database,
    a 404 Not Found error is raised.

    :param db: Session: Get the database session
    :param comment_id: int: Get the comment id from the path
    :return: A commentresponse object
    :doc-author: Trelent
    """
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

    """
    The edit_comment function allows a user to edit their own comment.
        The function takes in the body of the comment, which is a CommentModel object, and an integer representing
        the id of the comment that will be edited. It also takes in two dependencies: db and current_user.

    :param body: CommentModel: Specify the data that will be sent in the request body
    :param comment_id: int: Get the id of the comment to be deleted
    :param db: Session: Access the database
    :param current_user: User: Get the user who is currently logged in
    :return: The edited comment
    :doc-author: Trelent
    """
    comment = await comment_repository.edit_comments(comment_id, body, db, current_user)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(RoleChecker([UserRole.Admin.name, UserRole.Moderator.name]))])
async def delete_contact(comment_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):

    """
    The delete_contact function deletes a contact from the database.

    :param comment_id: int: Get the comment id from the url path
    :param db: Session: Get the database session
    :param current_user: User: Get the user that is currently logged in
    :return: A 204 status code
    :doc-author: Trelent
    """
    await comment_repository.delete_comments(comment_id, db)
