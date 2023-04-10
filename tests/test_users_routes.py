import pytest

from src.database.models import User, UserRole


@pytest.fixture()
def user():
    return {
        "id": "1",
        "username": "deadpool", 
        "email": "test1@example.com", 
        "password": "testtest", 
        "first_name": "test1",
        "last_name": "test1", 
        "user_role": "Admin"
        }


@pytest.fixture()
def token(user, client, session):
    client.post("/api/auth/signup", json=user)
    c: User = session.query(User).filter(User.email == user['email']).first()
    c.user_role = UserRole.Admin.name
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user['email'], "password": user['password']},
    )
    data = response.json()
    return data["access_token"]



def test_get_contacts(client):
    response = client.get(
        "/api/users/all"
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)


def test_get_user_profile_not_found(client, user):
    response = client.get(
        f"/api/users/get_user_profile?username={user['username']}"
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Not Found"
    

def test_update_user_self(client, token):
    response = client.put(
        "/api/users/update_user_self",
        json={
        "username":"username",
        "first_name": "new_first_name",
        "last_name":"last_name",
        "email":"email@meta.ua",
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["first_name"] == "new_first_name"
    assert "id" in data

def test_update_user_as_admin(client, token):
    response = client.put(
        "/api/users/update_user_as_admin",
        json={
        "username":"username",
        "first_name": "new_first_name",
        "last_name":"last_name",
        "email":"email@meta.ua",
        "is_active":"true",
        "user_role": "User"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["user_role"] == "User"
    assert "id" in data
