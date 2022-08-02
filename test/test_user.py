from fastapi.testclient import TestClient
from main import app

def test_create_user_ok():
    client = TestClient(app)

    user = {
        "email": "email@email.com",
        "username": "username",
        "password": "password",
        "updated_at": "2022-08-02T16:57:37.475575",
        "created_at": "2022-08-02T16:57:37.475575",
        "status": True
    }

    response = client.post(
        '/api/v1/user/',
        json=user,
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data['email'] == user['email']
    assert data['username'] == user['username']

def test_create_user_duplicate_email():
    client = TestClient(app)

    user = {
        "email": "email2@email.com",
        "username": "username2",
        "password": "password",
        "updated_at": "2022-08-02T16:57:37.475575",
        "created_at": "2022-08-02T16:57:37.475575",
        "status": True
    }

    response = client.post(
        '/api/v1/user/',
        json=user,
    )
    assert response.status_code == 201, response.text

    user['username'] = 'username3'

    response = client.post(
        '/api/v1/user/',
        json=user,
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data['detail'] == 'Email already registered'


def test_create_user_duplicate_username():
    client = TestClient(app)

    user = {
        "email": "email3@email.com",
        "username": "username4",
        "password": "password",
        "updated_at": "2022-08-02T16:57:37.475575",
        "created_at": "2022-08-02T16:57:37.475575",
        "status": True
    }

    response = client.post(
        '/api/v1/user/',
        json=user,
    )
    assert response.status_code == 201, response.text

    response = client.post(
        '/api/v1/user/',
        json=user,
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data['detail'] == 'Username already registered'