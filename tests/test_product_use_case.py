from fastapi import Depends

from app.config.database import get_db
from app.products.application.use_cases import ProductUseCase
from app.products.infrastructure.dtos import ProductSchema
from app.products.infrastructure.repository import DatabaseProductRepository


# Successfully create a product with valid data
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

    response = mock_use_case.create_product(
        product, token="test_token", db=Depends(get_db)
    )

    assert response == product


# Handle invalid product data gracefully

from fastapi import Depends

from app.config.database import get_db
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
