from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(min_length=2, max_length=15)
    first_name: str = Field(min_length=2, max_length=15)
    last_name: str = Field(min_length=2, max_length=15)
    email: EmailStr


class UserCreate(UserBase):
    username: str = Field(min_length=2, max_length=30)
    password: str = Field(min_length=6)


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}


class UserModel(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    number_of_photos: int

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    

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
