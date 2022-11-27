import json

import pytest
import requests

base_url = "http://127.0.0.1:8000"

data_to_seed = [
    {
        "reserved_for": "Jack",
        "reserved_by": "Bernard",
        "start_datetime": "2023-11-22T12:30:18",
        "end_datetime": "2023-11-22T12:30:18"
    },
    {
        "reserved_for": "Bill",
        "reserved_by": "Bernard",
        "start_datetime": "2023-11-22T12:30:18",
        "end_datetime": "2023-11-22T12:30:18"
    }
]


@pytest.fixture(scope="session")
def create_reservation():
    def _(reservation):
        r = requests.Session()
        response = r.post(url=f"{base_url}/create", params=reservation)
        assert response.status_code == 200
    return _


@pytest.fixture(scope="session")
def delete_reservation():
    def _(name):
        r = requests.Session()
        response = r.post(url=f"{base_url}/delete/{name}")
        assert response.status_code == 200

    return _


@pytest.fixture(scope="session")
def get_reservation():
    r = requests.Session()
    response = r.post(url=f"{base_url}/get")
    assert response.status_code == 200
    return response.json()


@pytest.fixture(scope="session")
def seed_server():
    r = requests.Session()
    for item in data_to_seed:
        response = r.post(url=f"{base_url}/create", params=item)
        assert response.status_code == 200, "Unable to seed server with test data"
    yield True
    for item in data_to_seed:
        _ = r.delete(url=f"{base_url}/{item['reserved_for']}")
