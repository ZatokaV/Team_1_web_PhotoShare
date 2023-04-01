import pytest
from unittest.mock import MagicMock

from src.database.models import Post, User
from src.services.messages_templates import NOT_FOUND


@pytest.fixture()
def c_user():
    return {"username": "test", "email": "test@example.com", "password": "testtest", "first_name": "test",
            "last_name": "test"}

@pytest.fixture()
def token(c_user, client, session, monkeypatch):
    client.post("/api/auth/signup", json=c_user)
    response = client.post(
        "/api/auth/login",
        data={"username": c_user['email'], "password": c_user['password']},
    )
    data = response.json()
    return data["access_token"]

@pytest.fixture()
def post_id(c_user, token, session):
    cur_user = session.query(User).filter(User.email == c_user['email']).first()
    print('USER ', cur_user.id, cur_user.username)
    post = session.query(Post).first()
    if post is None:
        post = Post(photo_url='PythonContactsApp/Irina', description='My new photo', user_id=cur_user.id)
        session.add(post)
        session.commit()
        session.refresh(post)
    return post.id


def test_transformation_for_image(post_id, client, token):
    url = 'https://res.cloudinary.com/drilpksk7/image/upload/e_grayscale:100/v1/PythonContactsApp/Irina'
    transformation = {"simple_effect": [{"effect": "grayscale", "strength": 100}]}
    response = client.post(f'/api/image/transform/{post_id}', json=transformation,  headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data.get('url') == url


def test_transformation_for_image_not_found(client, token):
    transformation = {"simple_effect": [{"effect": "grayscale", "strength": 100}]}
    response = client.post(f'/api/image/transform/9999', json=transformation,  headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404, response.text
    data = response.json()
    assert data.get('detail') == NOT_FOUND


def test_save_transform_image(post_id, client, token):
    url = 'https://res.cloudinary.com/drilpksk7/image/upload/e_grayscale:100/v1/PythonContactsApp/Irina'
    response = client.post(f'/api/image/transform/save/{post_id}', json={'url': url},  headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201, response.text
    data = response.json()
    assert data['photo_url'] == url


def test_get_qrcode_for_transform_image(post_id, client, token):
    qrcode = 'iVBORw0KGgoAAAANSUhEUgAAAeoAAAHqAQAAAADjFjCXAAADC0lEQVR4nO3aUY6jMAzGcUs9AEfi6hyJA1TKltifY9rdkUpYaR7+eWBayC99sZzYjLWZsRkcDofD4XA4/Ddxi/E4PdzNXhPsmPI0W/tl19QVDp/kq89/tD6/j7Yt/cEzuaYMAYfP8CMYVz173T4WWp6xUAnf15Qe3HD4jXzTM7OleQz3hVyucPj/4ArVmLBkqoTDb+b9T59w7Mg9ck2hGkvm1yHg8AkeQ2H5w8VOIQ2HX+ZlRICOJVUCe9C+TYbDL/OaIP0SSPt15ND3NeDwGb5rR+7Vb2zLsQ9HDHsg13oFDp/iLWOzlyV5b81zoKks8bL4I+bh8O94v+OdFh+lIm5xyUBW0QKHT/EekbW1sugNmqdPnRI9XjOHwuETvNzuI7Nkz5xtHBAd5dkQDr/ObZQgcSwUyk9Wt+9cCA6f4MsIy6fFQks+GGXxrmIYDp/lnhH3h4rcsi1HDMen9o/GCxx+geezcTbUQuOr/8xm9hG0cPglbvkfBP7JPgtfxTUcPs9b9o0jNlu0+0bSLLv0lg0aOHyK1xSonsvxZNcGvepnfDIcPslHgPqnVsqNjOZxSvwsRuDwr3mMDFDvw2R/b/xCywK5weFzvJ4De0R6RWzquYwXH/4zcPg89ybLqsKjvkbT15Iq//JmBA7/mpdZ3lpR+CqkI4dGWQKH38BPXT0rafEtS4624PlYCId/z+tUr36fVspiPyVqq25jwOETPOY/ouY1y7Q4XmgsTcdCOPwGHoXvEi/UWjt1X6I2aSOQVZbA4dd5tPvOHeQ+NtUhY13PpnD4JG8ekcqN8bbWC4+WbZlnXnJxOPwyL3VIFsMxQfEaaxxjLe/X4PCrfAw7d/WiSrH6LjfWgMPnuMJRW3AcEOOeVlNwR/cFDp/jPQRHRsyvMUuZ89Tzg8MneUe6XYJ2rBs51Kxu33D4DTxaeyqGPVX2dUv3rynM4fA7eHRaTKsdI5LmD8dCOPwK738Um5YHRH1Va9lXax+pEg7/nsfQhE0vdD1fZgvacsDhs/zqgMPhcDgcDof/Fv4HhwN5tI0WpSwAAAAASUVORK5CYII='
    response = client.get(f'/api/image/transform/qrcode/{post_id}',  headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == qrcode


def test_get_transformed_image(post_id, client, token):
    url = 'https://res.cloudinary.com/drilpksk7/image/upload/e_grayscale:100/v1/PythonContactsApp/Irina'
    response = client.get(f'/api/image/transform/{post_id}',  headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['photo_url'] == url


def test_get_list_of_transformed_image(post_id, client, token):
    response = client.get(f'/api/image/transform/all/{post_id}',  headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert type(data) == list


def test_remove_transformed_image(post_id, client, token):
    response = client.delete(f'/api/image/transform/{post_id}',  headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204, response.text
