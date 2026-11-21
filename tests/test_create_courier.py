import allure
import pytest
import requests

from scooter import COURIER_URL, TIMEOUT, new_courier


@allure.feature("Создание курьера")
class TestCreateCourier:
    @allure.title("Нового курьера можно создать")
    def test_create_courier(self, created_couriers):
        courier = new_courier()
        response = requests.post(COURIER_URL, json=courier, timeout=TIMEOUT)

        assert response.status_code == 201, response.text
        created_couriers.append(courier)
        body = response.json()
        assert set(body) == {"ok"}
        assert body["ok"] is True

    @allure.title("Регистрация без обязательного поля {field} возвращает 400")
    @pytest.mark.parametrize("field", ["login", "password", "firstName"])
    def test_missing_required_field(self, created_couriers, field):
        payload = new_courier()
        del payload[field]

        response = requests.post(COURIER_URL, json=payload, timeout=TIMEOUT)
        # Стенд может создать курьера даже без обязательного поля.
        if response.status_code == 201:
            created_couriers.append(payload)

        assert response.status_code == 400, response.text
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Повторная регистрация возвращает 409 ({param_id})")
    @pytest.mark.parametrize("change_details", [
        pytest.param(False, id="полный дубликат"),
        pytest.param(True, id="занят только логин"),
    ])
    def test_duplicate_login(self, registered_courier, created_couriers, change_details):
        payload = registered_courier.copy()
        if change_details:
            payload.update(password="другой-пароль", firstName="Другой")

        response = requests.post(COURIER_URL, json=payload, timeout=TIMEOUT)
        if response.status_code == 201:
            created_couriers.append(payload)

        assert response.status_code == 409, response.text
        assert response.json()["message"].startswith("Этот логин уже используется")
