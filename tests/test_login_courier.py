import allure
import pytest
import requests

from scooter import LOGIN_URL, TIMEOUT, credentials, new_courier


@allure.feature("Логин курьера")
class TestLoginCourier:
    @allure.title("Курьер входит в систему и получает числовой id")
    def test_login(self, registered_courier):
        payload = credentials(registered_courier)
        response = requests.post(LOGIN_URL, json=payload, timeout=TIMEOUT)

        assert response.status_code == 200, response.text
        courier_id = response.json()["id"]
        assert type(courier_id) is int and courier_id > 0

    @allure.title("Вход без обязательного поля {field} возвращает 400")
    @pytest.mark.parametrize("field", ["login", "password"])
    def test_missing_required_field(self, registered_courier, field):
        payload = credentials(registered_courier)
        del payload[field]

        response = requests.post(LOGIN_URL, json=payload, timeout=TIMEOUT)

        assert response.status_code == 400, response.text
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Вход с неверным значением {field} возвращает 404")
    @pytest.mark.parametrize("field", ["login", "password"])
    def test_incorrect_credentials(self, registered_courier, field):
        payload = credentials(registered_courier)
        payload[field] = new_courier()[field]

        response = requests.post(LOGIN_URL, json=payload, timeout=TIMEOUT)

        assert response.status_code == 404, response.text
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Вход с данными незарегистрированного курьера возвращает 404")
    def test_unknown_courier(self):
        payload = credentials(new_courier())
        response = requests.post(LOGIN_URL, json=payload, timeout=TIMEOUT)

        assert response.status_code == 404, response.text
        assert response.json()["message"] == "Учетная запись не найдена"
