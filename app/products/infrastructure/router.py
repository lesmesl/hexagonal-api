from typing import List

from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.orm import Session

from app.config.config import settings
from app.config.database import get_db
from app.products.application.use_cases import ProductUseCase
from app.products.infrastructure.dtos import ProductSchema
from app.products.infrastructure.repository import DatabaseProductRepository
from app.users.application.use_cases import oauth2_scheme

router = APIRouter()


@router.post(
    settings.REGISTER_PRODUCTS_ROUTE,
    response_model=ProductSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(oauth2_scheme)],
)
def create_product(
    product: ProductSchema,
    db: Session = Depends(get_db),
):
    repository = DatabaseProductRepository(db)
    use_case = ProductUseCase(repository)

    return use_case.create_product(product)


@router.get(
    settings.GET_PRODUCTS_ROUTE,
    response_model=List[ProductSchema],
    status_code=status.HTTP_200_OK,
)
def get_all_products(db: Session = Depends(get_db)):
    repository = DatabaseProductRepository(db)
    use_case = ProductUseCase(repository)
    return use_case.get_all_products()
