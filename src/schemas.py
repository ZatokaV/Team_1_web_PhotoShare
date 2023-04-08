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


class UserUpdate(UserBase):
    is_active: bool
    user_role: str


class UserModel(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    user_role: str

    class Config:
        orm_mode = True


class UserProfileModel(UserBase):
    id: int
    created_at: datetime
    is_active: bool
    number_of_photos: int

    class Config:
        orm_mode = True


class TagBase(BaseModel):
    tag: str


class TagCreate(TagBase):
    pass


class TagModel(TagBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    user_id: Optional[int]

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class PostBase(BaseModel):
    photo_url: str
    description: Optional[str]
    tags: Optional[List[TagBase]]


class PostCreate(PostBase):
    pass


class PostModel(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
    tags: Optional[List[TagModel]]

    class Config:
        orm_mode = True


class CommentModel(BaseModel):
    comment_text: str = Field("comment_text")


class CommentBase(BaseModel):
    id: int
    comment_text: Optional[str]
    created_at: datetime
    updated_at: datetime | None
    user_id: int

    class Config:
        orm_mode = True


class CommentResponse(BaseModel):
    comment: CommentBase
    user_first_name: str
    user_last_name: str
    username: str
    user_avatar: str | None


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


class SortType(str, Enum):
    rate = 'rate'
    date = 'date'


class SortUserType(str, Enum):
    date = 'date'
    name = 'name'
    username = 'username'
    email = 'email'


class SearchModel(BaseModel):
    search_str: str = Field(default='')
    sort: SortType = Field(default=SortType.date)
    sort_type: int = Field(ge=-1, le=1, default=1)


class SearchUserModel(BaseModel):
    search_str: str = Field(default='')
    sort: SortUserType = Field(default=SortUserType.username)
    sort_type: int = Field(ge=-1, le=1, default=1)


class TagType(BaseModel):
    id: int
    tag: str


class SearchResponse(PostBase, BaseModel):
    id: int
    photo_url: str
    description: Optional[str]
    user_id: int
    username: str
    created_at: datetime
    updated_at: datetime
    rate: int
    tags: Optional[List[TagType]]
