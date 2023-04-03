import pytest

from src.database.models import Post, User, RatePost
from src.services.messages_templates import NOT_FOUND


@pytest.fixture()
def c_user():
    return {"username": "test", "email": "test@example.com", "password": "testtest", "first_name": "test",
            "last_name": "test"}


@pytest.fixture()
def sec_user():
    return {"username": "test1", "email": "test1@example.com", "password": "testtest", "first_name": "test1",
            "last_name": "test1", "user_role": "Admin"}



@pytest.fixture()
def token(sec_user, client, session, monkeypatch):
    client.post("/api/auth/signup", json=sec_user)
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


def test_set_rates_for_posts(client, token, post_id):
    response = client.post(f'/api/rate/{post_id}', json={'rate': 3}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201, response.text
    data = response.json()
    assert data['rate'] == 3
    assert data['photo_id'] == post_id


def test_get_rates_for_current_user(client, token):
    response = client.get('/api/rate', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert type(data) == list
    assert len(data) == 1


def test_get_rate_from_user(client, token):
    response = client.get('/api/rate/user/1', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert type(data) == list


def test_get_rates_for_image(client, token, post_id):
    response = client.get(f'/api/rate/{post_id}', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert type(data) == list
    assert len(data) == 1


def test_remove_rate(client, token):
    response = client.delete('/api/rate/1', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204, response.text
