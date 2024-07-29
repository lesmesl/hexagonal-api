from app.config.config import settings


def test_create_product_success(client_with_db, test_login_token):

    token = test_login_token

    product_data = {
        "name": "Test Product",
        "price": 10.2,
        "in_stock": True,
        "description": "",
    }

    response = client_with_db.post(
        f"{settings.API_V1_URL}{settings.REGISTER_PRODUCTS_ROUTE}",
        json=product_data,
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201
    response_json = response.json()
    assert response_json["name"] == product_data["name"]
    assert response_json["description"] == product_data["description"]
    assert response_json["price"] == product_data["price"]


def test_create_product_invalid_data(client_with_db, test_login_token):

    token = test_login_token

    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": "invalid_price",  # Invalid price type
    }

    response = client_with_db.post(
        f"{settings.API_V1_URL}{settings.GET_PRODUCTS_ROUTE}",
        json=product_data,
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 422  # Unprocessable Entity
    response_json = response.json()
    assert "detail" in response_json


def test_create_product_invalid_data(client_with_db, test_login_token):

    token = test_login_token

    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": "invalid_price",  # Invalid price type
    }

    response = client_with_db.post(
        f"{settings.API_V1_URL}{settings.GET_PRODUCTS_ROUTE}",
        json=product_data,
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 422  # Unprocessable Entity
    response_json = response.json()
    assert "detail" in response_json


def test_create_product_unauthorized(client_with_db):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 10.2,
    }

    response = client_with_db.post(
        f"{settings.API_V1_URL}{settings.REGISTER_PRODUCTS_ROUTE}",
        json=product_data,
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 401  # Unauthorized
    response_json = response.json()
    assert "detail" in response_json


def test_get_all_products_unauthorized(
    client_with_db, test_create_product_success, data_product_success
):

    response = client_with_db.get(
        f"{settings.API_V1_URL}{settings.GET_PRODUCTS_ROUTE}",
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )

    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, list)
    assert len(response_json) > 0
    assert response_json[0]["name"] == data_product_success["name"]
    assert response_json[0]["description"] == data_product_success["description"]
    assert response_json[0]["price"] == data_product_success["price"]
    assert response_json[0]["in_stock"] == data_product_success["in_stock"]
