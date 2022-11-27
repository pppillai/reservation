import requests

from tests.test_utils import show_reservation, delete_reservation, create_reservation


def test_user_is_able_to_book_reservation(seed_server,
                                          client,
                                          seed_data):
    seed_server

    status, data = show_reservation(client)
    assert status == 200
    assert data
    total_data = len(data)
    status, response = delete_reservation(client, "Jack")
    assert status == 200
    status, data = show_reservation(client)
    assert len(data) < total_data
    reservation = {
            "reserved_for": "A",
            "reserved_by": "a",
            "start": "2021-11-22T12:30:18Z",
            "end": "2021-11-22T12:30:18Z"
        }
    status, response = create_reservation(client, reservation)
    assert status == 200
    status, response = create_reservation(client, reservation)
    assert status == 400
    status, response = delete_reservation(client, "A")
    assert status == 200

