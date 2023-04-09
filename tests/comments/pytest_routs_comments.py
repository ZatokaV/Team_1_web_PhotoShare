from unittest.mock import MagicMock, patch

import pytest

from src.database.models import Comment, User, Post, UserRole
from src.services.auth import auth_service


@pytest.fixture
def user():
    return {
        "username": "Deadpool",
        "first_name": "Dead",
        "last_name": "Pool",
        "email": "deadpool@example.com",
        "password": "1223334444"
    }


@pytest.fixture()
def admin():
    return {"username": "test1", "email": "test1@example.com", "password": "testtest", "first_name": "test1",
            "last_name": "test1", "user_role": "Admin"}


@pytest.fixture()
def admin_token(admin, client, session, monkeypatch):
    client.post("/api/auth/signup", json=admin)
    c: User = session.query(User).filter(User.email == admin['email']).first()
    c.user_role = UserRole.Admin.name
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": admin['email'], "password": admin['password']},
    )
    data = response.json()
    return data["access_token"]


@pytest.fixture()
def token(client, user, session):
    client.post("/api/auth/signup", json=user)
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    return data["access_token"]


def test_get_comments(client, session):
    # Create a test post and comment
    post_id = 1
    user = User(id=1, username="username", first_name="user_first_name", last_name="user_last_name",
                password="password")
    comment = Comment(post_id=post_id, comment_text="Test comment", user_id=user.id)
    session.add(user)
    session.add(comment)
    session.commit()

    # Make a request to the API endpoint
    response = client.get(f"/api/{post_id}/comments/")

    # Check that the response has a 200 status code
    assert response.status_code == 200

    # Check that the response contains the expected comment
    response_comment = response.json()[0]

    assert response_comment["comment"]["comment_text"] == "Test comment"


def test_add_comment(client, token, session):
    post = Post(id=1, description="This is a test post.", user_id=1)
    session.add(post)
    session.commit()

    comment_data = {"comment_text": "Test comment"}

    response = client.post(
        f"/api/{post.id}/comments/add_comment",
        json=comment_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201, response.text
    response_comment = response.json()
    assert response_comment["comment_text"] == comment_data["comment_text"]


def test_add_comment_not_found_post(client, token, session):
    post_id = 999

    comment_data = {"comment_text": "Test comment"}

    response = client.post(
        f"/api/{post_id}/comments/add_comment",
        json=comment_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404, response.text


def test_get_comment(client, session):
    # Create a test post and comment
    post_id = 1
    user = User(username="username", first_name="user_first_name", last_name="user_last_name",
                password="password")
    session.add(user)
    session.commit()

    comment = Comment(post_id=post_id, comment_text="Test comment", user_id=user.id)
    session.add(comment)
    session.commit()

    # Make a request to the API endpoint
    response = client.get(f"/api/{post_id}/comments/{comment.id}")

    # Check that the response has a 200 status code
    assert response.status_code == 200

    # Check that the response contains the expected comment
    response_comment = response.json()
    assert response_comment["comment"]["comment_text"] == "Test comment"


def test_edit_comment(client, session, token):
    # Create a post and comment to edit
    post_id = 1
    comment = Comment(id=1, post_id=post_id, comment_text="Test comment", user_id=1)
    session.add(comment)
    session.commit()

    headers = {"Authorization": f"Bearer {token}"}

    # Edit the comment
    new_comment_body = {"comment_text": "This is an edited comment."}
    response = client.patch(f"/api/{comment.post_id}/comments/{comment.id}/edit_comment", json=new_comment_body,
                            headers=headers)
    assert response.status_code == 200
    response_comment = response.json()
    assert response_comment["comment_text"] == comment.comment_text


def test_edit_comment_not_found_user(client, session, token):
    # Create a post and comment to edit
    comment = Comment(id=1, post_id=2, comment_text="Test comment", user_id=2)
    session.add(comment)
    session.commit()

    headers = {"Authorization": f"Bearer {token}"}

    # Edit the comment
    new_comment_body = {"comment_text": "This is an edited comment."}
    response = client.patch(f"/api/{comment.post_id}/comments/{comment.id}/edit_comment", json=new_comment_body,
                            headers=headers)
    assert response.status_code == 404


def test_delete_comment_admin(client, session, admin_token):
    post_id = 1
    comment = Comment(id=1, post_id=post_id, comment_text="Test comment", user_id=1)
    session.add(comment)
    session.commit()
    header = {"Authorization": f"Bearer {admin_token}"}
    response = client.delete(f"/api/{post_id}/comments/{comment.id}", headers=header)
    assert response.status_code == 204


def test_delete_comment_user(client, session, token):
    post_id = 1
    comment = Comment(id=1, post_id=post_id, comment_text="Test comment", user_id=1)
    session.add(comment)
    session.commit()
    header = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/api/{post_id}/comments/{comment.id}", headers=header)
    assert response.status_code == 403