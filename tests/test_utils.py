import json


def show_reservation(client):
    response = client.get(url=f"/show")
    return response.status_code, response.json()


def delete_reservation(client, name):
    response = client.delete(f"/delete/{name}")
    return response.status_code, response.json()


def create_reservation(client, payload):
    response = client.post(url=f"/create", data=json.dumps(payload))
    return response.status_code, response.json()
