import pytest

from src.database.models import Post, User, TransformPosts
import src.repository.transform_posts as rep_transform


@pytest.fixture(scope='module')
def current_user(user, session):
    cur_user = session.query(User).filter(User.email == user.get('email')).first()
    if cur_user is None:
        cur_user = User(email=user.get('email'), username=user.get('username'), password=user.get('password'))
        session.add(cur_user)
        session.commit()
        session.refresh(cur_user)
    return cur_user


@pytest.fixture(scope='module')
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
    response = await rep_transform.get_image_for_transform(post.id, session)
    assert response == post.photo_url


@pytest.mark.asyncio
async def test_get_image_for_transform_not_found(current_user, session):
    response = await rep_transform.get_image_for_transform(9999, session)
    assert response is None


@pytest.mark.asyncio
async def test_set_transform_image(post, session):
    url = 'https://res.cloudinary.com/drilpksk7/image/upload/e_grayscale:100/v1/PythonContactsApp/Irina'
    response = await rep_transform.set_transform_image(post.id, url, session)
    assert response.photo_url == url
    assert response.photo_id == post.id


@pytest.mark.asyncio
async def test_get_transform_image(post, session):
    t_post = session.query(TransformPosts).first()
    response = await rep_transform.get_transform_image(t_post.id, session)
    assert response.id == t_post.id
    assert response.photo_url == t_post.photo_url


@pytest.mark.asyncio
async def test_get_all_transform_images(post, session):
    l_post = session.query(TransformPosts).filter(TransformPosts.photo_id == post.id).all()
    response = await rep_transform.get_all_transform_images(post.id, session)
    assert response == l_post
