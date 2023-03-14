import pytest
from jose import jwt
from app import schemas
from app.config import settings

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

def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user["email"], "password": test_user["password"]}
    )

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("hello1@gmail.com", "wrong", 403),
    ("wrong@gmail.com", "test123", 403),
    ("hello1@gmail.com", None, 422),
    (None, "test123", 422),
])
def test_incorrect_user(email, password, status_code, client):
    res = client.post(
        "/login", data={"username": email, "password": password}
    )
    assert res.status_code == status_code
