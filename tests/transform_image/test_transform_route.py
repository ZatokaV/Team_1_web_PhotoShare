import pytest

from src.database.models import Post, User
from src.services.messages_templates import NOT_FOUND

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


def test_transformation_for_image(post, client, session):
    url = 'https://res.cloudinary.com/drilpksk7/image/upload/e_grayscale:100/v1/PythonContactsApp/Irina'
    transformation = {"simple_effect": [{"effect": "grayscale", "strength": 100}]}
    response = client.post(f'/api/image/transform/{post.id}', json=transformation)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data.get('url') == url


def test_transformation_for_image_not_found(post, client):
    transformation = {"simple_effect": [{"effect": "grayscale", "strength": 100}]}
    response = client.post(f'/api/image/transform/9999', json=transformation)
    assert response.status_code == 404, response.text
    data = response.json()
    assert data.get('detail') == NOT_FOUND


def test_save_transform_image(post, client):
    url = 'https://res.cloudinary.com/drilpksk7/image/upload/e_grayscale:100/v1/PythonContactsApp/Irina'
    response = client.post(f'/api/image/transform/save/{post.id}', json={'url': url})
    assert response.status_code == 201, response.text
    data = response.json()
    assert data['photo_url'] == url


def test_get_qrcode_for_transform_image(post, client):
    qrcode = 'iVBORw0KGgoAAAANSUhEUgAAAeoAAAHqAQAAAADjFjCXAAADC0lEQVR4nO3aUY6jMAzGcUs9AEfi6hyJA1TKltifY9rdkUpYaR7+eWBayC99sZzYjLWZsRkcDofD4XA4/Ddxi/E4PdzNXhPsmPI0W/tl19QVDp/kq89/tD6/j7Yt/cEzuaYMAYfP8CMYVz173T4WWp6xUAnf15Qe3HD4jXzTM7OleQz3hVyucPj/4ArVmLBkqoTDb+b9T59w7Mg9ck2hGkvm1yHg8AkeQ2H5w8VOIQ2HX+ZlRICOJVUCe9C+TYbDL/OaIP0SSPt15ND3NeDwGb5rR+7Vb2zLsQ9HDHsg13oFDp/iLWOzlyV5b81zoKks8bL4I+bh8O94v+OdFh+lIm5xyUBW0QKHT/EekbW1sugNmqdPnRI9XjOHwuETvNzuI7Nkz5xtHBAd5dkQDr/ObZQgcSwUyk9Wt+9cCA6f4MsIy6fFQks+GGXxrmIYDp/lnhH3h4rcsi1HDMen9o/GCxx+geezcTbUQuOr/8xm9hG0cPglbvkfBP7JPgtfxTUcPs9b9o0jNlu0+0bSLLv0lg0aOHyK1xSonsvxZNcGvepnfDIcPslHgPqnVsqNjOZxSvwsRuDwr3mMDFDvw2R/b/xCywK5weFzvJ4De0R6RWzquYwXH/4zcPg89ybLqsKjvkbT15Iq//JmBA7/mpdZ3lpR+CqkI4dGWQKH38BPXT0rafEtS4624PlYCId/z+tUr36fVspiPyVqq25jwOETPOY/ouY1y7Q4XmgsTcdCOPwGHoXvEi/UWjt1X6I2aSOQVZbA4dd5tPvOHeQ+NtUhY13PpnD4JG8ekcqN8bbWC4+WbZlnXnJxOPwyL3VIFsMxQfEaaxxjLe/X4PCrfAw7d/WiSrH6LjfWgMPnuMJRW3AcEOOeVlNwR/cFDp/jPQRHRsyvMUuZ89Tzg8MneUe6XYJ2rBs51Kxu33D4DTxaeyqGPVX2dUv3rynM4fA7eHRaTKsdI5LmD8dCOPwK738Um5YHRH1Va9lXax+pEg7/nsfQhE0vdD1fZgvacsDhs/zqgMPhcDgcDof/Fv4HhwN5tI0WpSwAAAAASUVORK5CYII='
    response = client.get(f'/api/image/transform/qrcode/{post.id}')
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == qrcode


def test_get_transformed_image(post, client):
    url = 'https://res.cloudinary.com/drilpksk7/image/upload/e_grayscale:100/v1/PythonContactsApp/Irina'
    response = client.get(f'/api/image/transform/{post.id}')
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['photo_url'] == url


def test_get_list_of_transformed_image(post, client):
    response = client.get(f'/api/image/transform/all/{post.id}')
    assert response.status_code == 200, response.text
    data = response.json()
    assert type(data) == list

