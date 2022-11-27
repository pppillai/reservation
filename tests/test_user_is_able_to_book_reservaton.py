import requests


def test_user_is_able_to_book_reservation(seed_server, create_reservation, delete_reservation, get_reservation):
    seed_server()
    data = get_reservation()
    assert data
    delete_reservation("Jack")
    reservation = reservation = {
            "reserved_for": "A",
            "reserved_by": "a",
            "start_datetime": "2022-11-22T12:30:18Z",
            "end_datetime": "2022-11-22T12:30:18Z"
        }
    create_reservation(reservation)