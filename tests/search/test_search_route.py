import pytest

from src.database.models import Post, User, UserRole


@pytest.fixture()
def c_user(session):
    return {"username": "test", "email": "test@example.com", "password": "testtest", "first_name": "test",
            "last_name": "test", "user_role": "User"}


@pytest.fixture()
def sec_user():
    return {"username": "test1", "email": "test1@example.com", "password": "testtest", "first_name": "test1",
            "last_name": "test1", "user_role": "Admin"}


@pytest.fixture()
def token(sec_user, client, session, monkeypatch):

    client.post("/api/auth/signup", json=sec_user)
    c: User = session.query(User).filter(User.email == sec_user['email']).first()
    c.user_role = UserRole.Admin.name
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": sec_user['email'], "password": sec_user['password']},
    )
    data = response.json()
    return data["access_token"]


@pytest.fixture()
def cur_token(c_user, client, session, monkeypatch):
    client.post("/api/auth/signup", json=c_user)
    response = client.post(
        "/api/auth/login",
        data={"username": c_user['email'], "password": c_user['password']},
    )
    data = response.json()
    return data["access_token"]


@pytest.fixture()
def post_id(c_user, cur_token, session):
    cur_user = session.query(User).filter(User.email == c_user['email']).first()
    post = session.query(Post).first()
    if post is None:
        post = Post(photo_url='PythonContactsApp/Irina', description='My new photo', user_id=cur_user.id)
        session.add(post)
        session.commit()
        session.refresh(post)
    return post.id


def test_search_posts(client, token, post_id):
    response = client.post('/api/search', json={"search_str": "My", "sort": "rate", "sort_type": 1},
                           headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]['id'] == post_id

