from typing import List

from sqlalchemy import or_, func, text, desc
from sqlalchemy.orm import Session

from src.database.models import Post, Tag, post_tag, RatePost, User
from src.services.cloudynary import get_url
from src.schemas import SearchResponse, SortUserType, SortType


async def get_search_posts(search_str: str, sort: str, sort_type: int, skip: int, limit: int, db: Session)\
        -> List[SearchResponse]:
    search_list = []
    search_list.append(Post.description.ilike(f'%{search_str}%'))
    search_list.append(Tag.tag.ilike(f'%{search_str}%'))
    sql = db.query(Post, User.username, func.coalesce(func.avg(RatePost.rate), 0).label('rate')) \
        .select_from(Post).join(User).join(RatePost, isouter=True).join(post_tag, isouter=True).join(Tag, isouter=True)\
        .filter(or_(*search_list)) \
        .group_by(Post, User.username)
    if sort == SortType.rate.name:
        if sort_type == -1:
            sql = sql.order_by(desc('rate'))
        else:
            sql = sql.order_by('rate')
    if sort == SortType.date.name:
        if sort_type == -1:
            sql = sql.order_by(desc(Post.created_at))
        else:
            sql = sql.order_by(Post.created_at)
    posts = sql.offset(skip).limit(limit).all()
    result = []
    for post in posts:
        item = {x.name: getattr(post[0], x.name) for x in post[0].__table__.columns}
        item['username'] = post[1]
        item['rate'] = post[2]
        item['photo_url'] = get_url(item['photo_url'])
        tags = db.query(Tag).join(post_tag).join(Post).filter(Post.id == item['id']).order_by(Tag.tag).all()
        item['tags'] = [{'id': tag.id, 'tag': tag.tag} for tag in tags]
        result.append(item)
    return result


async def get_search_users(search_str: str, sort: str, sort_type: int, skip: int, limit: int, db: Session):
    list_reg = []
    list_reg.append(User.username.ilike(f"%{search_str}%"))
    list_reg.append(User.first_name.ilike(f"%{search_str}%"))
    list_reg.append(User.last_name.ilike(f"%{search_str}%"))
    list_reg.append(User.email.ilike(f"%{search_str}%"))
    sql = db.query(User).filter(or_(*list_reg))
    if sort == SortUserType.username.name:
        if sort_type == -1:
            sql = sql.order_by(desc(SortUserType.username.name))
        else:
            sql = sql.order_by(SortUserType.username.name)
    if sort == SortUserType.date.name:
        if sort_type == -1:
            sql = sql.order_by(desc(User.created_at))
        else:
            sql = sql.order_by(User.created_at)
    if sort == SortUserType.email.name:
        if sort_type == -1:
            sql = sql.order_by(desc(User.email))
        else:
            sql = sql.order_by(User.email)
    if sort == SortUserType.name.name:
        if sort_type == -1:
            sql = sql.order_by(desc(User.first_name, User.last_name))
        else:
            sql = sql.order_by(User.first_name, User.last_name)
    users = sql.offset(skip).limit(limit).all()
    return users
