from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel
from pydantic import EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(min_length=2, max_length=15)
    first_name: str = Field(min_length=2, max_length=15)
    last_name: str = Field(min_length=2, max_length=15)
    email: EmailStr


class UserCreate(UserBase):
    username: str = Field(min_length=2, max_length=25)
    email: EmailStr
    password: str = Field(min_length=6)


class UserModel(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    user_role: Enum

    class Config:
        orm_mode = True


class UserProfileModel(UserBase):
    id: int
    created_at: datetime
    number_of_photos: int
    is_active: bool

    class Config:
        orm_mode = True


class TagBase(BaseModel):
    tag: str


class TagCreate(TagBase):
    pass


class TagModel(TagBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class PostBase(BaseModel):
    photo_url: Optional[str]
    description: Optional[str]
    tags: Optional[List[TagCreate]]


class PostCreate(PostBase):
    pass


class PostModel(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
    comments: Optional[List["CommentModel"]] = []

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    comment_url: Optional[str]
    comment_text: Optional[str]


class CommentCreate(CommentBase):
    pass


class CommentModel(CommentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
    post_id: int

    class Config:
        orm_mode = True


class RateCreate(BaseModel):
    rate: int = Field(ge=1, le=5)


class RateDB(BaseModel):
    id: int
    rate: int
    user_id: int
    photo_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class RateResponse(RateDB, BaseModel):
    username: str
    photo_url: str
