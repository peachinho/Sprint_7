import pytest
import requests

from scooter import COURIER_URL, LOGIN_URL, ORDERS_URL, TIMEOUT, credentials, new_courier


@pytest.fixture
def courier_registrations():
    registrations = []
    yield registrations
    for courier, response in registrations:
        if response.status_code != 201:
            continue
        if "login" not in courier or "password" not in courier:
            continue
        login = requests.post(LOGIN_URL, json=credentials(courier), timeout=TIMEOUT)
        login.raise_for_status()
        courier_id = login.json()["id"]
        removed = requests.delete(f"{COURIER_URL}/{courier_id}", timeout=TIMEOUT)
        removed.raise_for_status()


@pytest.fixture
def registered_courier(courier_registrations):
    courier = new_courier()
    response = requests.post(COURIER_URL, json=courier, timeout=TIMEOUT)
    response.raise_for_status()
    courier_registrations.append((courier, response))
    return courier


@pytest.fixture
def created_order_tracks():
    tracks = []
    yield tracks
    for track in tracks:
        cancelled = requests.put(f"{ORDERS_URL}/cancel", params={"track": track}, timeout=TIMEOUT)
        cancelled.raise_for_status()
