import allure
import pytest
import requests
import jsonschema
from test.schemas.order_schema import ORDER_SCHEMA
from test.schemas.inventory_schema import INVENTORY_SCHEMA
BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:
    @allure.title("проверка размещения заказа в магазине")
    def test_place_a_new_order_in_the_store(self):
        with allure.step("Подготовка данных для размещения заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса на размещение заказа"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()

        with allure.step("Проверка статус-кода и структуры ответа"):
            assert response.status_code == 200
            jsonschema.validate(instance=response_json, schema=ORDER_SCHEMA)

        with allure.step("Проверка корректности данных заказа в ответе"):
            assert response_json["id"] == payload["id"]
            assert response_json["petId"] == payload["petId"]
            assert response_json["quantity"] == payload["quantity"]
            assert response_json["status"] == payload["status"]
            assert response_json["complete"] == payload["complete"]

    @allure.title("Получение информации о заказе по ID")
    def test_get_info_by_id (self,create_order):
        with allure.step("Получение ID созданного заказа"):
                order_id = create_order["id"]
        with allure.step("отправка запроса на получение информации о заказе по ID"):
                response = requests.get(f"{BASE_URL}/store/order/{order_id}")
        with allure.step("проверка статуса  ответа и данных заказа"):
                assert response.status_code == 200
                assert response.json()["id"] == order_id

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id (self,create_order):
        with allure.step("Получение ID  заказа из ответа"):
            order_id = create_order["id"]

        with allure.step("удаление заказа"):
            response = requests.delete(url=f"{BASE_URL}/store/order/1")

        with allure.step("проверка статуса  ответа"):
            assert response.status_code == 200

        with allure.step("отправка запроса на уделенный заказ"):
            response = requests.get(url=f"{BASE_URL}/store/order/1")

        with allure.step("проверка статуса  ответа"):
            assert response.status_code == 404

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order(self):
        with allure.step("отправка запроса на получение информации о несуществующем заказа"):
            response = requests.get(url=f"{BASE_URL}/store/order/99999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404


    @allure.title("Получение инвентаря магазина")
    def test_get_store_inventory(self):
        with allure.step("отправка запроса на получение инвентаря"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")
            response_json = response.json()

        with allure.step("проверка ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(instance=response_json, schema=INVENTORY_SCHEMA)










