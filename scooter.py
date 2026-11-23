from datetime import date, timedelta
from uuid import uuid4


BASE_URL = "https://qa-scooter.education-services.ru/api/v1"
COURIER_URL = f"{BASE_URL}/courier"
LOGIN_URL = f"{COURIER_URL}/login"
ORDERS_URL = f"{BASE_URL}/orders"
TIMEOUT = 30


def new_courier():
    return {
        "login": f"sprint7_{uuid4().hex}",
        "password": uuid4().hex,
        "firstName": "Тест",
    }


def credentials(courier):
    return {"login": courier["login"], "password": courier["password"]}


def new_order():
    return {
        "firstName": "Тест",
        "lastName": "Спринт",
        "address": "Учебная улица, 7",
        "metroStation": "4",
        "phone": "+7 000 000 00 00",
        "rentTime": 1,
        "deliveryDate": (date.today() + timedelta(days=1)).isoformat(),
        "comment": "Учебный заказ Sprint_7",
    }
