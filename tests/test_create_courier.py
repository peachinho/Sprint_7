import allure
import pytest
import requests

from scooter import COURIER_URL, TIMEOUT, new_courier


@allure.feature("Создание курьера")
class TestCreateCourier:
    @allure.title("Нового курьера можно создать")
    def test_create_courier(self, courier_registrations):
        courier = new_courier()
        response = requests.post(COURIER_URL, json=courier, timeout=TIMEOUT)
        courier_registrations.append((courier, response))

        assert response.status_code == 201, response.text
        body = response.json()
        assert set(body) == {"ok"}
        assert body["ok"] is True

    @allure.title("Регистрация без обязательного поля {field} возвращает 400")
    @pytest.mark.parametrize("field", ["login", "password", "firstName"])
    def test_missing_required_field(self, courier_registrations, field):
        payload = new_courier()
        del payload[field]

        response = requests.post(COURIER_URL, json=payload, timeout=TIMEOUT)
        courier_registrations.append((payload, response))

        assert response.status_code == 400, response.text
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Повторная регистрация того же курьера возвращает 409")
    def test_duplicate_courier(self, registered_courier, courier_registrations):
        response = requests.post(COURIER_URL, json=registered_courier, timeout=TIMEOUT)
        courier_registrations.append((registered_courier, response))

        assert response.status_code == 409, response.text
        assert response.json()["message"].startswith("Этот логин уже используется")

    @allure.title("Регистрация с занятым логином и другими данными возвращает 409")
    def test_duplicate_login(self, registered_courier, courier_registrations):
        payload = registered_courier.copy()
        payload.update(password="другой-пароль", firstName="Другой")

        response = requests.post(COURIER_URL, json=payload, timeout=TIMEOUT)
        courier_registrations.append((payload, response))

        assert response.status_code == 409, response.text
        assert response.json()["message"].startswith("Этот логин уже используется")
