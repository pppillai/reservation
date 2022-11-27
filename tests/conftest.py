import datetime
import json

import pytest
import requests

r = requests.Session()
base_url = "http://127.0.0.1:8000"
utc_now = datetime.datetime.utcnow()
date_format = "%Y-%m-%dT%H:%M:%SZ"
data_to_seed = [
    {
        "reserved_for": "Jack",
        "reserved_by": "Bernard",
        "start": (utc_now + datetime.timedelta(weeks=52)).strftime(date_format),
        "end": (utc_now + datetime.timedelta(weeks=52, hours=1)).strftime(date_format)
    },
    {
        "reserved_for": "Bill",
        "reserved_by": "Bernard",
        "start": (utc_now + datetime.timedelta(weeks=53)).strftime(date_format),
        "end": (utc_now + datetime.timedelta(weeks=53, hours=1)).strftime(date_format)
    }
]


@pytest.fixture(scope="session")
def seed_server():
    for item in data_to_seed:
        response = r.post(url=f"{base_url}/create", data=json.dumps(item))
        assert response.status_code == 200, "Unable to seed server with test data"
    yield True
    for item in data_to_seed:
        _ = r.delete(url=f"{base_url}/{item['reserved_for']}")


@pytest.fixture(scope="function")
def show_reservation():
    response = r.get(url=f"{base_url}/show")
    return response.status_code, response.json()


@pytest.fixture(scope="function")
def delete_reservation():
    def _(name):
        response = r.delete(url=f"{base_url}/reservaton/{name}")
        return response.status_code, response.json()
    return _

@pytest.fixture(scope="function")
def create_reservation():
    def _(payload):
        response = r.post(url=f"{base_url}/create", data=json.dumps(payload))
        return response.status_code, response.json()
    return _