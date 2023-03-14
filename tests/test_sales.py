import pytest
from typing import List
from app import schemas


def test_get_all_sales(authorized_client, test_sales):
    res = authorized_client.get("/sales/")

    assert res.status_code == 200
    assert len(res.json()) == len(test_sales)

def test_unauthorized_user_get_all_sales(client):
    res = client.get("/sales/")

    assert res.status_code == 401


def test_get_one_sale(authorized_client, test_sales):
    res = authorized_client.get(f"/sales/{test_sales[0].id}")
    sale = schemas.SaleBase(**res.json()["Sale"])

    assert sale.total == test_sales[0].total
    assert res.status_code == 200

def test_unauthorized_user_get_one_sale(client, test_sales):
    res = client.get(f"/sales/{test_sales[0].id}")

    assert res.status_code == 401

def test_unauthorized_user_get_one_sale_not_exist(authorized_client):
    res = authorized_client.get(f"/sales/9999")

    assert res.status_code == 404

@pytest.mark.parametrize("total, payment_method, credit", [
    (50.99, "credit", True),
    (45.99, "cash", False)
])
def test_create_sale(authorized_client, total, payment_method, credit, test_user):
    res = authorized_client.post("/sales/", json={"total": total, "payment_method": payment_method, "credit": credit})
    created_sale = schemas.Sale(**res.json())

    assert res.status_code == 201
    assert created_sale.total == total
    assert created_sale.user.id == test_user['id']

def test_create_sale_default_payment_method(authorized_client, test_user):
    res = authorized_client.post("/sales/", json={"total": 50, "payment_method": 'cash'})
    created_sale = schemas.Sale(**res.json())

    assert res.status_code == 201
    assert created_sale.user.id == test_user['id']