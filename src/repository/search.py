from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from src.database.models import Post, Tag, post_tag, RatePost


async def get_search_posts(search_str: str, sort: str, sort_type: int, skip: int, limit: int, db: Session):
    search_list = []
    search_list.append(Post.description.ilike(f'%{search_str}%'))
    search_list.append(Tag.tag.ilike(f'%{search_str}%'))
    sql = db.query(Post.id, func.avg(RatePost.rate).label('rate'))\
        .select_from(Post).join(post_tag).join(Tag).join(RatePost)\
        .filter(or_(*search_list)).group_by(Post, post_tag, Tag)
    print(sql)
    print(sql.all())