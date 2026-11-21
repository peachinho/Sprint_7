import allure
import pytest
import requests

from scooter import ORDERS_URL, TIMEOUT, new_order


@allure.feature("Создание заказа")
@allure.title("Создание заказа возвращает track ({param_id})")
@pytest.mark.parametrize("colors", [
    pytest.param(["BLACK"], id="BLACK"),
    pytest.param(["GREY"], id="GREY"),
    pytest.param(["BLACK", "GREY"], id="BLACK и GREY"),
    pytest.param(None, id="поле color отсутствует"),
    pytest.param([], id="пустой список цветов"),
])
def test_create_order_returns_track(created_order_tracks, colors):
    payload = new_order()
    if colors is not None:
        payload["color"] = colors

    response = requests.post(ORDERS_URL, json=payload, timeout=TIMEOUT)

    assert response.status_code == 201, response.text
    track = response.json()["track"]
    assert type(track) is int
    created_order_tracks.append(track)


@allure.feature("Список заказов")
@allure.title("Первая страница заказов содержит массив orders")
def test_list_orders():
    response = requests.get(ORDERS_URL, params={"page": 0, "limit": 1}, timeout=TIMEOUT)

    assert response.status_code == 200
    assert isinstance(response.json()["orders"], list)
