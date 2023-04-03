import pytest
from sqlalchemy import and_

import src.repository.rates as rep_rate
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
def third_user():
    return {"username": "test2", "email": "test2@example.com", "password": "testtest", "first_name": "test2",
            "last_name": "test2", "user_role": "User"}


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
def second_user(third_user, session):
    user = session.query(User).filter(User.email == third_user.get('email')).first()
    if user is None:
        user = User(email=third_user.get('email'), username=third_user.get('username'),
                    password=third_user.get('password'), user_role=third_user.get('user_role'))
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
async def test_set_rate_for_image(post, session, second_user):
    response = await rep_rate.set_rate_for_image(post.id, 4, second_user, session)
    assert response.photo_id == post.id
    assert response.user_id == second_user.id


@pytest.mark.asyncio
async def test_set_rate_for_own_image(post, session, current_user):
    response = await rep_rate.set_rate_for_image(post.id, 4, current_user, session)
    assert response is None


@pytest.mark.asyncio
async def test_remove_rate_for_image(post, second_user, session):
    response = await rep_rate.remove_rate_for_image(1, second_user, session)
    assert response.id == 1
    assert response.user_id == second_user.id
    assert response.photo_id == post.id


@pytest.mark.asyncio
async def test_remove_rate_for_image_as_admin(post, second_user, admin_user, session):
    rate = await rep_rate.set_rate_for_image(post.id, 4, second_user, session)
    response = await rep_rate.remove_rate_for_image(rate.id, admin_user, session)
    assert response.id == rate.id
    assert response.user_id == second_user.id
    assert response.photo_id == post.id


@pytest.mark.asyncio
async def test_remove_rate_for_image_as_other_user(post, second_user, current_user, session):
    rate = await rep_rate.set_rate_for_image(post.id, 4, second_user, session)
    response = await rep_rate.remove_rate_for_image(rate.id, current_user, session)
    assert response is None


@pytest.mark.asyncio
async def test_get_rate_for_image(post, current_user, second_user, admin_user, session):
    rates =[]
    rates.append(await rep_rate.set_rate_for_image(post.id, 4, second_user, session))
    rates.append(await rep_rate.set_rate_for_image(post.id, 5, admin_user, session))
    response = await rep_rate.get_rate_for_image(post.id, current_user, session)
    assert len(response) == len(rates)


@pytest.mark.asyncio
async def test_get_rate_for_image_as_admin(post, current_user, second_user, admin_user, session):
    rates =[]
    rates.append(await rep_rate.set_rate_for_image(post.id, 4, second_user, session))
    rates.append(await rep_rate.set_rate_for_image(post.id, 5, admin_user, session))
    response = await rep_rate.get_rate_for_image(post.id, admin_user, session)
    assert len(response) == len(rates)


@pytest.mark.asyncio
async def test_get_rate_for_image_as_other_user(post, current_user, second_user, admin_user, session):
    rates =[]
    rates.append(await rep_rate.set_rate_for_image(post.id, 4, second_user, session))
    rates.append(await rep_rate.set_rate_for_image(post.id, 5, admin_user, session))
    response = await rep_rate.get_rate_for_image(post.id, second_user, session)
    assert response == []


@pytest.mark.asyncio
async def test_get_rate_for_user(second_user, post, session):
    response = await rep_rate.get_rate_for_user(second_user, session)
    assert len(response) == 1
    assert response[0].rate == '4'


@pytest.mark.asyncio
async def test_get_rate_for_user_as_admin(admin_user, post, session):
    response = await rep_rate.get_rate_for_user(admin_user, session)
    assert len(response) == 1
    assert response[0].rate == '5'


@pytest.mark.asyncio
async def test_get_rate_from_user(admin_user, second_user, session):
    response = await rep_rate.get_rate_from_user(second_user.id, admin_user, session)
    assert len(response) == 1
    assert response[0].rate == '4'
    assert response[0].user_id == second_user.id


@pytest.mark.asyncio
async def test_get_rate_from_user_not_admin(current_user, second_user, session):
    response = await rep_rate.get_rate_from_user(second_user.id, current_user, session)
    assert response == []
