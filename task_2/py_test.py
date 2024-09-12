import pytest
import requests

# Определим базовый URL микросервиса
BASE_URL = "https://qa-internship.avito.com/api/1"


# Тест кейсы

# test_create_ad_success: Проверяет успешное создание объявления. Проверяет, что 
# ответ содержит код 200 и уникальный идентификатор объявления.
def test_create_ad_success():
    url = f"{BASE_URL}/item"
    payload = {
        "name": "Телефон",
        "price": 85566,
        "sellerId": 3452,
        "statistics": {
            "contacts": 32,
            "like": 35,
            "viewCount": 14
        }
    }

    response = requests.post(url, json=payload)

    assert response.status_code == 200
    assert 'Сохранили объявление' in response.json().get('status', '')


# test_create_ad_missing_fields: Проверяет, что система возвращает ошибку 500 и
# текствое представление ошибки.
def test_create_ad_missing_fields():
    url = f"{BASE_URL}/item"
    payload = {
        "name": "Телефон",
        "price": 85566
    }

    response = requests.post(url, json=payload)

    assert response.status_code == 500
    assert "internal error" in response.json().get('message', '')
    assert 500 == response.json().get('code', '')


# test_get_ad_success: Проверяет успешное получение объявления по его id.
# Проверяет, что все необходимые поля присутствуют в ответе.
def test_get_ad_success():
    create_url = f"{BASE_URL}/item"
    create_payload = {
        "name": "Телефон",
        "price": 85566,
        "sellerId": 3452,
        "statistics": {
            "contacts": 32,
            "like": 35,
            "viewCount": 14
        }
    }

    item_id = _create_post(create_url, create_payload)

    url = f"{BASE_URL}/item/{item_id}"

    response = requests.get(url)

    assert response.status_code == 200
    items = response.json()

    assert len(items) == 1
    item_by_id = items[0]
    assert item_by_id['name'] == "Телефон"
    assert item_by_id['id'] == item_id
    assert item_by_id['price'] == 85566
    assert item_by_id['sellerId'] == 3452
    assert item_by_id['statistics']['contacts'] == 32
    assert item_by_id['statistics']['likes'] == 0
    assert item_by_id['statistics']['viewCount'] == 14


# test_get_ad_not_found: Проверяет, что система возвращает ошибку 404
# при запросе несуществующего объявления.
def test_get_ad_not_found():
    ad_id = "99999999-9999-9999-9999-999999999999"
    url = f"{BASE_URL}/item/{ad_id}"

    response = requests.get(url)

    assert response.status_code == 404
    assert "404" == response.json().get('status', '')
    assert "not found" in response.json().get('result', '').get('message', '')


# test_get_ads_by_seller_success: Проверяет успешное получение всех объявлений по sellerID.
# Проверяет, что ответ содержит массив объявлений с необходимыми полями.
def test_get_ads_by_seller_success():
    seller_id = 3452
    create_url = f"{BASE_URL}/item"
    create_payload = {
        "name": "Телефон",
        "price": 85566,
        "sellerId": seller_id,
        "statistics": {
            "contacts": 32,
            "like": 35,
            "viewCount": 14
        }
    }
    _ = _create_post(create_url, create_payload)

    url = f"{BASE_URL}/{seller_id}/item"
    response = requests.get(url)

    print(response.json())
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    if items:
        assert 'id' in items[0]
        assert 'name' in items[0]
        assert 'price' in items[0]
        assert 'statistics' in items[0]
        assert 'sellerId' in items[0]
        assert 'contacts' in items[0]['statistics']
        assert 'likes' in items[0]['statistics']
        assert 'viewCount' in items[0]['statistics']


# test_get_ads_by_seller_not_found: Проверяет, что система возвращает 200 OK и пустой массив
# при запросе объявлений для несуществующего продавца.
def test_get_ads_by_seller_not_found():
    seller_id = -1222
    url = f"{BASE_URL}/{seller_id}/item"

    response = requests.get(url)

    assert response.status_code == 200
    assert len(response.json()) == 0


def _create_post(url, payload) -> str:
    response = requests.post(url, json=payload)

    return response.json().get("status", "").split()[-1]
