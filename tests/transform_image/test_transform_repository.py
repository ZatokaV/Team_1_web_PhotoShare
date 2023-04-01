import pytest

from src.database.models import Post, User, TransformPosts
import src.repository.transform_posts as rep_transform

@pytest.fixture()
def c_user():
    return {"username": "test", "email": "test@example.com", "password": "testtest", "first_name": "test",
            "last_name": "test"}


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
async def test_get_transform_image(post, current_user, session):
    t_post = session.query(TransformPosts).first()
    response = await rep_transform.get_transform_image(t_post.id, current_user, session)
    assert response.id == t_post.id
    assert response.photo_url == t_post.photo_url


@pytest.mark.asyncio
async def test_get_all_transform_images(post, current_user, session):
    l_post = session.query(TransformPosts).filter(TransformPosts.photo_id == post.id).all()
    response = await rep_transform.get_all_transform_images(post.id, current_user, session)
    assert response == l_post
