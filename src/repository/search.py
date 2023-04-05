from sqlalchemy import or_, func, text, desc
from sqlalchemy.orm import Session

from src.database.models import Post, Tag, post_tag, RatePost, User


async def get_search_posts(search_str: str, sort: str, sort_type: int, skip: int, limit: int, db: Session):
    search_list = []
    search_list.append(Post.description.ilike(f'%{search_str}%'))
    search_list.append(Tag.tag.ilike(f'%{search_str}%'))
    sql = db.query(Post.id, Post.photo_url, Post.description, Post.user_id, Post.created_at, Post.updated_at, Tag.id,
                   Tag.tag, User.id, User.username, func.coalesce(func.avg(RatePost.rate), 0).label('rate'))\
        .select_from(Post).join(RatePost, isouter=True).join(post_tag, isouter=True).join(Tag, isouter=True).join(User)\
        .filter(or_(*search_list))\
        .group_by(Post.id, Post.photo_url, Post.description, Post.user_id, Tag.id, Tag.tag, User.id, User.username,
                  Post.created_at, Post.updated_at)
    if sort == 'rate':
        if sort_type == -1:
            sql = sql.order_by(desc('rate'))
        else:
            sql = sql.order_by('rate')
    if sort == 'date':
        if sort_type == -1:
            sql = sql.order_by(desc(Post.created_at))
        else:
            sql = sql.order_by(Post.created_at)
    posts = sql.all()

    return posts


    print(posts)
