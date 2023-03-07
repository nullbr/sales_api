from app import schemas
from .database import client, session

def test_root(client):
    res = client.get("/")
    print(res.json())
    assert res.json().get('Sales') == 'API'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello1@gmail.com", "password": "test123"}
    )
    new_user = schemas.User(**res.json())
    assert new_user.email == "hello1@gmail.com"
    assert res.status_code == 201

def test_login_user(client):
    res = client.post(
        "/login", data={"username": "hello1@gmail.com", "password": "test123"}
    )
    assert res.status_code == 200