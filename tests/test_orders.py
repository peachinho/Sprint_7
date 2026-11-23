import allure
import pytest
import requests

from scooter import ORDERS_URL, TIMEOUT, new_order


class TestOrders:
    @allure.feature("Создание заказа")
    @allure.title("Создание заказа возвращает track ({param_id})")
    @pytest.mark.parametrize("color_fields", [
        pytest.param({"color": ["BLACK"]}, id="BLACK"),
        pytest.param({"color": ["GREY"]}, id="GREY"),
        pytest.param({"color": ["BLACK", "GREY"]}, id="BLACK и GREY"),
        pytest.param({}, id="поле color отсутствует"),
        pytest.param({"color": []}, id="пустой список цветов"),
    ])
    def test_create_order_returns_track(self, created_order_tracks, color_fields):
        payload = new_order()
        payload.update(color_fields)

        response = requests.post(ORDERS_URL, json=payload, timeout=TIMEOUT)

        assert response.status_code == 201, response.text
        track = response.json()["track"]
        assert type(track) is int
        created_order_tracks.append(track)

    @allure.feature("Список заказов")
    @allure.title("Первая страница заказов содержит массив orders")
    def test_list_orders(self):
        response = requests.get(ORDERS_URL, params={"page": 0, "limit": 1}, timeout=TIMEOUT)

        assert response.status_code == 200
        assert isinstance(response.json()["orders"], list)
