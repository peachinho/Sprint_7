import pytest
import requests

from scooter import COURIER_URL, LOGIN_URL, ORDERS_URL, TIMEOUT, credentials, new_courier


@pytest.fixture
def created_couriers():
    couriers = []
    yield couriers
    for courier in couriers:
        login = requests.post(LOGIN_URL, json=credentials(courier), timeout=TIMEOUT)
        assert login.status_code == 200, login.text
        courier_id = login.json()["id"]
        removed = requests.delete(f"{COURIER_URL}/{courier_id}", timeout=TIMEOUT)
        assert removed.status_code == 200, removed.text
        assert removed.json()["ok"] is True


@pytest.fixture
def registered_courier(created_couriers):
    courier = new_courier()
    response = requests.post(COURIER_URL, json=courier, timeout=TIMEOUT)
    assert response.status_code == 201, response.text
    created_couriers.append(courier)
    return courier


@pytest.fixture
def created_order_tracks():
    tracks = []
    yield tracks
    for track in tracks:
        cancelled = requests.put(f"{ORDERS_URL}/cancel", params={"track": track}, timeout=TIMEOUT)
        assert cancelled.status_code == 200, cancelled.text
        assert cancelled.json()["ok"] is True
