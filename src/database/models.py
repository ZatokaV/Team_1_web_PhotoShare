import enum

from sqlalchemy import Column, Integer, String, Text, ForeignKey, func, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()


class UserRole(int, enum.Enum):
    Admin = 1
    Moderator = 2
    User = 3


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    first_name = Column(String(70))
    last_name = Column(String(70))
    email = Column(String(250), unique=True)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    user_role = Column(Integer, default=UserRole.User.name)


post_tag = Table('post_tag',
                 Base.metadata,
                 Column("id", Integer, primary_key=True),
                 Column("post", Integer, ForeignKey(
                     "posts.id", ondelete="CASCADE")),
                 Column("tag", Integer, ForeignKey(
                     "tags.id", ondelete="CASCADE")),
                 )


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    photo_url = Column(String())
    description = Column(Text)
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"))
    marked = Column(Boolean, default=False)  # deletion mark
    tags = relationship("Tag", secondary=post_tag,
                        backref="posts", passive_deletes=True)
    user = relationship('User', backref="photos")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    comment_text = Column(Text)
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime)

    post_id = Column(Integer, ForeignKey(Post.id, ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey(User.id))

    user = relationship('User', backref="comments")
    post = relationship('Post', backref="comments")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    tag = Column(String(25), unique=True)
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"))

    user = relationship('User', backref="tags")


class TransformPosts(Base):
    __tablename__ = 'transform_posts'

    id = Column(Integer, primary_key=True)
    photo_url = Column(String, nullable=False)
    photo_id = Column(Integer, ForeignKey(Post.id, ondelete="CASCADE"))
    created_at = Column('created_at', DateTime, default=func.now())

    post = relationship('Post', backref="transform_posts")


class RatePost(Base):
    __tablename__ = 'rates_posts'

    id = Column(Integer, primary_key=True)
    rate = Column("rate", Integer, default=0)
    photo_id = Column(Integer, ForeignKey(Post.id, ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"))
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())

    post = relationship('Post', backref="rates_posts")
    user = relationship('User', backref="rates_posts")
