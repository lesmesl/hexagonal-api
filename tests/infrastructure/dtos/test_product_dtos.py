import pytest
from pydantic import ValidationError

from app.products.application.use_cases import ProductUseCase
from app.products.infrastructure.dtos import ProductCreateSchema
from app.products.infrastructure.repository import DatabaseProductRepository


def test_product_schema_create_success(mocker):
    """
    Prueba que un ProductCreateSchema se cree con éxito con datos válidos.
    """
    product_data = {
        "name": "Test Product",
        "price": 10.99,
        "in_stock": True,
        "description": "A test product",
    }
    product = ProductCreateSchema(**product_data)

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


def test_product_schema_create_invalid_name():
    """
    Prueba que la creación de un ProductCreateSchema falle con un nombre inválido.
    """
    invalid_product_data = {
        "name": 12123,  # Nombre inválido, debería ser una cadena de texto
        "price": 10.99,
        "in_stock": True,
        "description": "",
    }

    with pytest.raises(ValidationError):
        ProductCreateSchema(**invalid_product_data)


def test_product_schema_create_invalid_price():
    """
    Prueba que la creación de un ProductCreateSchema falle con un precio negativo.
    """
    invalid_product_data = {
        "name": "test",
        "price": -10.99,  # Precio inválido, debería ser positivo
        "in_stock": True,
        "description": "",
    }

    with pytest.raises(ValidationError) as exc_info:
        ProductCreateSchema(**invalid_product_data)

    error = exc_info.value.errors()
    assert error[0]["loc"] == ("price",)
    assert "Value error, Price must be positive" in error[0]["msg"]
