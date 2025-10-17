from http.client import responses
import allure
import jsonschema
import requests
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ответа не совпадает с ожидаемым"

    @allure.title("попытка обновить не существующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("отправка запроса на обновление несуществующего питомца"):
            payload = {"id": 9999,
                       "name": "Non-existent Pet",
                       "status": "available"
                       }

            response = requests.put(url=f"{BASE_URL}/pet", json=payload)
        assert response.status_code == 404, "код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпадает с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step("отправка запроса на получение информации о несуществующем питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/99999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпадает с ожидаемым"

    @allure.title("добавление нового питомца")
    def test_add_new_pet(self):
        with allure.step("подготовка данных для создания питомца"):
            payload = {"id": 1,
                       "name": "Buddy",
                       "status": "available"
                       }
        with allure.step("отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("проверка ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response.json(), PET_SCHEMA)

        with allure.step("проверка параметров питомца в ответе"):
            assert response_json["id"] == payload["id"]
            assert response_json["name"] == payload["name"]
            assert response_json["status"] == payload["status"]


    @allure.title("добавление нового питомца с подготовкой полных данных")
    def test_add_new_whole_pet(self):
        with allure.step("подготовка  всех данных для создания питомца"):
            payload =  {"id": 10,
                       "name": "doggie",
                       "category":{
                           "id": 1,
                            "name": "Dogs"},
                       "photoUrls": ["string"],
                       "tags": [
                           {"id": 0, "name": "string"}
                       ],
                       "status": "available"
                       }
        with allure.step("отправка запроса на создание питомца с полными данными"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("проверка ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response.json(), PET_SCHEMA)

        with allure.step("проверка полных параметров питомца в ответе"):
            assert response_json["id"] == payload["id"]
            assert response_json["name"] == payload["name"]
            assert response_json["category"] == payload["category"]
            assert response_json["photoUrls"] == payload["photoUrls"]
            assert response_json["status"] == payload["status"]
            assert response_json["tags"] == payload["tags"]
            for tag in payload["tags"]:
                assert tag in response_json["tags"]



    @allure.title("получение информации о питомце по ID")
    def test_get__pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("проверка статуса  ответа и данных питомца"):
            assert response.status_code == 200
            assert response.json()["id"] == pet_id


    @allure.title("Обновление информации о питомце ")
    def test_update_pet_information(self, create_pet):

        with allure.step("отправка запроса на создание питомца с полными данными"):
            response = requests.post(url=f"{BASE_URL}/pet", json=create_pet)
            response_json = response.json()


        with allure.step("Получение ID  питомца"):
            pet_id = create_pet["id"]



        with allure.step("проверка статуса  ответа"):
            assert response.status_code == 200


        with allure.step("подготовка данных для обновления информации питомца"):
            payload =  {"id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }
        with allure.step("отправка запроса на питомца с обновленными  данными"):
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("проверка статуса  ответа и обновленных данных питомца"):
            assert response.status_code == 200
            assert response_json["id"] == payload["id"]
            assert response_json["name"] == payload["name"]
            assert response_json["status"] == payload["status"]





    @allure.title("Удаление питомца по ID")
    def test_delete_pet_by_id(self, create_pet):
        with allure.step("Получение ID  питомца из ответа"):
            pet_id = create_pet["id"]

        with allure.step("удаление питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")


        with allure.step("проверка статуса  ответа"):
            assert response.status_code == 200

        with allure.step("отправка запроса на уделенного питомца"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")


        with allure.step("проверка статуса  ответа"):
            assert response.status_code == 404
