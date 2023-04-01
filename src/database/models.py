import enum
from sqlalchemy import Column, Integer, String, Text, ForeignKey, func, Table, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime


Base = declarative_base()


class UserRole(enum.Enum):
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
    # user_role = Column(Enum(UserRole), default=UserRole.User)


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

    tags = relationship("Tag", secondary=post_tag,
                        backref="posts", passive_deletes=True)
    user = relationship('User', backref="photos")


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    comment_url = Column(String())
    comment_text = Column(Text)
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())

    post_id = Column(Integer, ForeignKey(Post.id, ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"))

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
