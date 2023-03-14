from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db
from app.database import Base
from app.main import app
from app.oauth2 import create_acesss_token
from app import models

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    # run code befor test run
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # run code after test finishes

@pytest.fixture
def test_user(client):
    user_data = {"email": "hello1@gmail.com", "password": "test123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    
    new_user = res.json()
    new_user["password"] = user_data["password"]
    
    return new_user

@pytest.fixture
def token(test_user):
    return create_acesss_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_sales(test_user, session):
    sales_data = [
        {
            "total": 120.21,
            "payment_method": "credit",
            "credit": True,
            "user_id": test_user['id']
        },
        {
            "total": 40.25,
            "payment_method": "debit",
            "credit": False,
            "user_id": test_user['id']
        },
        {
            "total": 500.50,
            "payment_method": "cash",
            "credit": False,
            "user_id": test_user['id']
        },
    ]

    def create_sale_model(sale):
        return models.Sale(**sale)

    sales = list(map(create_sale_model, sales_data))


    session.add_all(sales)
    session.commit()

    return session.query(models.Sale).all()
