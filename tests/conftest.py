import datetime
import json

import pytest
from requests_toolbelt import sessions

utc_now = datetime.datetime.utcnow()
date_format = "%Y-%m-%dT%H:%M:%SZ"


@pytest.fixture(scope="session")
def seed_server(client, seed_data):
    for item in seed_data:
        response = client.post(url=f"/create", data=json.dumps(item))
        assert response.status_code == 200, "Unable to seed server with test data"
    yield True
    for item in seed_data:
        _ = client.delete(url=f"/delete/{item['reserved_for']}")


@pytest.fixture(scope="session")
def client():
    r = sessions.BaseUrlSession(base_url="http://127.0.0.1:8000")
    return r


@pytest.fixture(scope="session")
def seed_data():
    data = [
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
    return data
