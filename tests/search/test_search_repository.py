from typing import List

import pytest

import src.repository.search as rep_search
from src.database.models import Post, User, RatePost, UserRole


@pytest.fixture()
def c_user():
    return {"username": "test", "email": "test@example.com", "password": "testtest", "first_name": "test",
            "last_name": "test", "user_role": "User"}


@pytest.fixture()
def sec_user():
    return {"username": "test1", "email": "test1@example.com", "password": "testtest", "first_name": "test1",
            "last_name": "test1", "user_role": "Admin"}


@pytest.fixture()
def current_user(c_user, session):
    cur_user = session.query(User).filter(User.email == c_user.get('email')).first()
    if cur_user is None:
        cur_user = User(email=c_user.get('email'), username=c_user.get('username'), password=c_user.get('password'),
                        user_role=c_user.get('user_role'))
        session.add(cur_user)
        session.commit()
        session.refresh(cur_user)
    return cur_user


@pytest.fixture()
def admin_user(sec_user, session):
    user = session.query(User).filter(User.email == sec_user.get('email')).first()
    if user is None:
        user = User(email=sec_user.get('email'), username=sec_user.get('username'), password=sec_user.get('password'),
                    user_role=sec_user.get('user_role'))
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


@pytest.fixture()
def post(current_user, session):
    post = session.query(Post).first()
    if post is None:
        post = Post(photo_url='PythonContactsApp/Irina', description='My new photo', user_id=current_user.id)
        session.add(post)
        session.commit()
        session.refresh(post)
    return post


@pytest.mark.asyncio
async def test_get_search_posts_date(post, session):
    response = await rep_search.get_search_posts('My', 'date', 1, 0, 20, session)
    assert type(response) == list
    assert response[0]['id'] == post.id


@pytest.mark.asyncio
async def test_get_search_posts_date_desc(post, session):
    response = await rep_search.get_search_posts('My', 'date', -1, 0, 20, session)
    assert type(response) == list
    assert response[0]['id'] == post.id


@pytest.mark.asyncio
async def test_get_search_posts_rate(post, session):
    response = await rep_search.get_search_posts('My', 'rate', 1, 0, 20, session)
    assert type(response) == list
    assert response[0]['id'] == post.id


@pytest.mark.asyncio
async def test_get_search_posts_rate_desc(post, session):
    response = await rep_search.get_search_posts('My', 'rate', -1, 0, 20, session)
    assert type(response) == list
    assert response[0]['id'] == post.id

@pytest.mark.asyncio
async def test_get_search_users_date(c_user, session):
    response = await rep_search.get_search_users('test', 'date', 1, 0, 20, session)
    assert type(response) == list
    assert response[0].username == c_user['username']


@pytest.mark.asyncio
async def test_get_search_users_name_desc(c_user, session):
    response = await rep_search.get_search_users('test', 'name', -1, 0, 20, session)
    assert type(response) == list
    assert response[0].username == c_user['username']


@pytest.mark.asyncio
async def test_get_search_users_email(c_user, session):
    response = await rep_search.get_search_users('test', 'email', 1, 0, 20, session)
    assert type(response) == list
    assert response[0].username == c_user['username']
