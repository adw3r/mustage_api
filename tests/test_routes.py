import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    return TestClient(app)

def test_get_all(client):
    response = client.get("/payments")
    print(response.text)
    assert response.status_code == 200

def test_get_payment_with_date(client):
    response = client.get("/payments", params={"created_at": "2025-04-01"})
    print(response.text)
    assert response.status_code == 200

def test_wrong_input(client):
    response = client.get("/payments", params={"created_at": "01.12.1310"})
    print(response.text)
    assert response.status_code == 422


def test_insert_payment(client):
    """
    :param client:
    :return:
    """
    response = client.post("/payments", json={
        'created_at': '19.03.2025',
        'comment': 'test',
        'amount_uah': '24',

    })
    print(response.text)
    assert response.status_code == 200

def test_insert_wrong_date_payment(client):
    """
    :param client:
    :return:
    """
    response = client.post("/payments", json={
        'created_at': '191234.03123123.2131232025',
        'comment': 'test',
        'amount_uah': '24',

    })
    print(response.text)
    assert response.status_code == 422
    response = client.post("/payments", json={
        'created_at': '191234.03123123.2131232025',
        'comment': '123125215125123123',
        'amount_uah': 'awdawdawdawd',

    })
    print(response.text)
    assert response.status_code == 422

def test_delete_payment(client):
    payment_id = 2
    response = client.delete(f"/payments/{payment_id}")
    print(response.text)
    assert response.status_code == 204


def test_patch_payment(client):
    payment_id = 1
    response = client.patch(f"/payments/{payment_id}", json={
        'comment': 'test',
        'amount_uah': 23

    })
    print(response.text)
    assert response.status_code == 200
