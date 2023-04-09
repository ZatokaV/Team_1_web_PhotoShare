import pytest

import src.repository.transform_posts as rep_transform
from src.database.models import Post, User, TransformPosts


@pytest.fixture()
def c_user():
    return {"username": "test", "email": "test@example.com", "password": "testtest", "first_name": "test",
            "last_name": "test"}


@pytest.fixture()
def sec_user():
    return {"username": "test1", "email": "test1@example.com", "password": "testtest", "first_name": "test1",
            "last_name": "test1", "user_role": "Admin"}


@pytest.fixture()
def current_user(c_user, session):
    cur_user = session.query(User).filter(User.email == c_user.get('email')).first()
    if cur_user is None:
        cur_user = User(email=c_user.get('email'), username=c_user.get('username'), password=c_user.get('password'))
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
async def test_get_image_for_transform(current_user, post, session):
    response = await rep_transform.get_image_for_transform(post.id, current_user, session)
    assert response == post.photo_url


@pytest.mark.asyncio
async def test_get_image_for_transform_not_found(current_user, session):
    response = await rep_transform.get_image_for_transform(9999, current_user, session)
    assert response is None


@pytest.mark.asyncio
async def test_set_transform_image(post, current_user, session):
    url = 'https://res.cloudinary.com/drilpksk7/image/upload/e_grayscale:100/v1/PythonContactsApp/Irina'
    response = await rep_transform.set_transform_image(post.id, url, current_user, session)
    assert response.photo_url == url
    assert response.photo_id == post.id


@pytest.mark.asyncio
async def test_set_transform_image_not_found(post, current_user, session):
    url = 'https://res.cloudinary.com/drilpksk7/image/upload/e_grayscale:100/v1/PythonContactsApp/Irina'
    response = await rep_transform.set_transform_image(999, url, current_user, session)
    assert response is None


@pytest.mark.asyncio
async def test_get_transform_image(post, current_user, session):
    t_post = session.query(TransformPosts).first()
    response = await rep_transform.get_transform_image(t_post.id, current_user, session)
    assert response.id == t_post.id
    assert response.photo_url == t_post.photo_url


@pytest.mark.asyncio
async def test_get_transform_image_not_found(current_user, session):
    response = await rep_transform.get_transform_image(999, current_user, session)
    assert response is None


@pytest.mark.asyncio
async def test_get_all_transform_images(post, current_user, session):
    t_post = session.query(TransformPosts).first()
    l_post = session.query(TransformPosts).filter(TransformPosts.photo_id == t_post.id).all()
    response = await rep_transform.get_all_transform_images(post.id, 0, 20, current_user, session)
    assert response == l_post


@pytest.mark.asyncio
async def test_get_all_transform_images_not_found(current_user, session):
    response = await rep_transform.get_all_transform_images(999, 0, 20, current_user, session)
    assert response == []



@pytest.mark.asyncio
async def test_remove_transform_image(current_user, session):
    t_post = session.query(TransformPosts).first()
    response = await rep_transform.remove_transform_image(t_post.id, current_user, session)
    assert response.id == t_post.id
    assert response.photo_url == t_post.photo_url


@pytest.mark.asyncio
async def test_remove_transform_image(admin_user, session):
    t_post = session.query(TransformPosts).first()
    response = await rep_transform.remove_transform_image(t_post.id, admin_user, session)
    assert response.id == t_post.id
    assert response.photo_url == t_post.photo_url


@pytest.mark.asyncio
async def test_remove_transform_image_not_found(current_user, session):
    response = await rep_transform.remove_transform_image(999, current_user, session)
    assert response is None


@pytest.mark.asyncio
async def test_get_all_transform_images_for_user(current_user, session):
    l_post = session.query(TransformPosts).all()
    response = await rep_transform.get_all_transform_images_for_user(0, 20, current_user, session)
    assert response == l_post


@pytest.mark.asyncio
async def test_get_all_transform_images_for_user_as_admin(admin_user, session):
    l_post = session.query(TransformPosts).all()
    response = await rep_transform.get_all_transform_images_for_user(0, 20, admin_user, session)
    assert response == l_post
