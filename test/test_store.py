import allure
import pytest
import requests

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:
    @allure.title("проверка размещения заказа в магазине")
    def test_place_a_new_order_in_the_store(self,create_order):
            with allure.step("Отправка запроса на размещение заказа"):
                response = requests.post(url=f"{BASE_URL}/store/order",json=create_order)
                response_json = response.json()
            with allure.step("Проверка статуса ответа и данных заказа"):
                assert response.status_code == 200
                assert response_json["id"] == create_order["id"]
                assert response_json["petId"] == create_order["petId"]
                assert response_json["quantity"] == create_order["quantity"]
                assert response_json["status"] == create_order["status"]
                assert response_json["complete"] == create_order["complete"]

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
    @pytest.mark.parametrize(
        "expected_data, expected_status_code",
        [
            ({"approved": 57, "delivered": 50}, 200) #в Swagger в примере эндпоинта данных больше чем в требованиях самого теста, если это так и должно быть - ОК,если инфа устарела - я добавлю...ну либо я что - то не так поняла как делать +)))
        ]
    )
    def test_get_inventory(self,expected_data, expected_status_code):
        with allure.step("Запрос на получение инвентаря"):
             response = requests.get(url=f"{BASE_URL}/store/inventory")
        with allure.step("Проверка статуса ответа и формата данных"):
            assert response.status_code == expected_status_code
            assert isinstance(response.json(), dict)







