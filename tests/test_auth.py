from unittest.mock import MagicMock
import pytest

from src.database.models import User
from src.services.messages_templates import ALREADY_EXISTS, EMAIL_NOT_CONFIRMED, INVALID_PASSWORD, INVALID_EMAIL
from src.services.urls_templates import URL_SIGNUP, URL_LOGIN


@pytest.fixture
def user():
    return {
        "username": "Deadpool",
        "first_name": "Dead",
        "last_name": "Pool",
        "email": "deadpool@example.com",
        "password": "1223334444"
    }

def test_create_user(client, user):
    response = client.post(
        URL_SIGNUP,
        json=user,
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["user"]["email"] == user.get("email")
    assert "id" in data["user"]


def test_repeat_create_user(client, user):
    response = client.post(
        URL_SIGNUP,
        json=user,
    )
    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] == ALREADY_EXISTS



def test_login_user(client, session, user):
    current_user: User = session.query(User).filter(
        User.email == user.get('email')).first()
    session.commit()
    response = client.post(
        URL_LOGIN,
        data={"username": user.get('email'), "password": user.get('password')},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, user):
    response = client.post(
        URL_LOGIN,
        data={"username": user.get('email'), "password": 'password'},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == INVALID_PASSWORD


def test_login_wrong_email(client, user):
    response = client.post(
        URL_LOGIN,
        data={"username": 'email', "password": user.get('password')},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == INVALID_EMAIL
