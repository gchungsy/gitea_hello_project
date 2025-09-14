import requests

BASE_URL = "https://postman-echo.com"


def test_get_params():
    params = {"foo": "bar", "test": "123"}

    response = requests.get(f"{BASE_URL}/get", params=params)

    assert response.status_code == 200

    data = response.json()
    assert data["args"]["foo"] == "bar"
    assert data["args"]["test"] == "123"

def test_post_request():
    payload = {"username": "gary", "role": "qa"}
    response = requests.post(f"{BASE_URL}/post", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["json"]["username"] == "gary"
    assert data["json"]["role"] == "qa"
