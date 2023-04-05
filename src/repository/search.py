from sqlalchemy import or_, func, text, desc
from sqlalchemy.orm import Session

from src.database.models import Post, Tag, post_tag, RatePost, User
from src.services.cloudynary import get_url


async def get_search_posts(search_str: str, sort: str, sort_type: int, skip: int, limit: int, db: Session):
    search_list = []
    search_list.append(Post.description.ilike(f'%{search_str}%'))
    search_list.append(Tag.tag.ilike(f'%{search_str}%'))
    sql = db.query(Post, User.username, func.coalesce(func.avg(RatePost.rate), 0).label('rate')) \
        .select_from(Post).join(User).join(RatePost, isouter=True).join(post_tag, isouter=True).join(Tag, isouter=True)\
        .filter(or_(*search_list)) \
        .group_by(Post, User.username)
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
    print(sql)
    posts = sql.all()
    result = []
    for post in posts:
        item = {x.name: getattr(post[0], x.name) for x in post[0].__table__.columns}
        item['username'] = post[1]
        item['rate'] = post[2]
        item['photo_url'] = get_url(item['photo_url'])
        tags = db.query(Tag).join(post_tag).join(Post).filter(Post.id == item['id']).order_by(Tag.tag).all()
        # item['tags'] = [{x.name: getattr(tag, x.name) for x in tag.__table__.columns} for tag in tags]
        item['tags'] = [{'id': tag.id, 'tag': tag.tag} for tag in tags]
        result.append(item)
    return result
