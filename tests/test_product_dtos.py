import pytest
from pydantic import ValidationError

from app.products.application.use_cases import ProductUseCase
from app.products.infrastructure.dtos import ProductSchema
from app.products.infrastructure.repository import DatabaseProductRepository


# Test para creación exitosa de un producto con datos válidos
def test_create_product_success(mocker):
    product_data = {
        "name": "Test Product",
        "price": 10.99,
        "in_stock": True,
        "description": "A test product",
    }
    product = ProductSchema(**product_data)

    mock_db = mocker.Mock()
    mock_repo = mocker.Mock(DatabaseProductRepository)
    mock_use_case = mocker.Mock(ProductUseCase)
    mock_use_case.create_product.return_value = product

    mocker.patch(
        "app.products.application.use_cases.ProductUseCase", return_value=mock_use_case
    )
    mocker.patch(
        "app.products.infrastructure.repository.DatabaseProductRepository",
        return_value=mock_repo,
    )
    mocker.patch("app.config.database.get_db", return_value=mock_db)

    response = mock_use_case.create_product(product)

    assert response == product


# Test para manejo de datos inválidos de producto
def test_create_product_invalid_data():
    # Datos de producto inválidos
    invalid_product_data = {
        "name": 12123,
        "price": 10.99,
        "in_stock": True,
        "description": "",
    }

    # Prueba de validación
    with pytest.raises(ValidationError):
        # Intentar crear un ProductSchema con datos inválidos debería lanzar ValidationError
        ProductSchema(**invalid_product_data)


def test_create_product_invalid_type_price():
    # Datos de producto inválidos
    invalid_product_data = {
        "name": "test",
        "price": -10.99,
        "in_stock": True,
        "description": "",
    }

    # Prueba de validación
    with pytest.raises(ValidationError) as exc_info:
        # Intentar crear un ProductSchema con datos inválidos debería lanzar ValidationError
        ProductSchema(**invalid_product_data)

    error = exc_info.value.errors()
    assert error[0]["loc"] == ("price",)
    assert "Value error, Price must be positive" in error[0]["msg"]
