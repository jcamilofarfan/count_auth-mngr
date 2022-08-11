from pipes import Template
from urllib import response
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

def test_login_user_ok():
    client = TestClient(app)
    user = {
        "email": "gustavo@email.com",
        "username": "gustavo",
        "password": "password",
        "updated_at": "2022-08-02T16:57:37.475575",
        "created_at": "2022-08-02T16:57:37.475575",
        "status": True
    }

    response = client.post(
        '/api/v1/user/',
        json=user,
    )

    login = {
        'grant_type': '',
        "username": "gustavo",
        "password": "password",
        'scope': '',
        'client_id': '',
        'client_secret': ''
    }
    response = client.post(
        '/api/v1/login/',
        data=login,
        headers={
            'content-type': 'application/x-www-form-urlencoded'
        },
        allow_redirects=True
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data['access_token'] is not None
    assert data['token_type'] == 'bearer'

def test_login_user_username_not_exist():
    client = TestClient(app)
    login = {
        'grant_type': '',
        "username": "gustavo20",
        "password": "password",
        'scope': '',
        'client_id': '',
        'client_secret': ''
    }
    response = client.post(
        '/api/v1/login/',
        data=login,
        headers={
            'content-type': 'application/x-www-form-urlencoded'
        },
        allow_redirects=True
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data['detail'] == 'Incorrect username or password'

def create_and_login_user(username:str):
    client = TestClient(app)
    user = {
        "email": f'{username}@pruebas.com',
        "username": username,
        "password": "password",
        "updated_at": "2022-08-02T16:57:37.475575",
        "created_at": "2022-08-02T16:57:37.475575",
        "status": True
    }

    response = client.post(
        '/api/v1/user/',
        json=user,
    )

    login = {
        'grant_type': '',
        "username": username,
        "password": "password",
        'scope': '',
        'client_id': '',
        'client_secret': ''
    }
    response = client.post(
        '/api/v1/login/',
        data=login,
        headers={
            'content-type': 'application/x-www-form-urlencoded'
        },
        allow_redirects=True
    )

    data = response.json()
    return data['access_token']

def test_refresh_token_user():
    token = create_and_login_user('test_refresh')
    client = TestClient(app)

    response = client.post(
        '/api/v1/login/refresh/',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['access_token'] is not None
    assert data['token_type'] == 'bearer'
