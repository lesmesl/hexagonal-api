from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.config import settings
from app.config.database import get_db
from app.products.application.use_cases import ProductUseCase
from app.products.infrastructure.dtos import ProductSchema
from app.products.infrastructure.repository import DatabaseProductRepository
from app.users.application.use_cases import oauth2_scheme

router = APIRouter()


@router.get(settings.PING_ROUTE)
async def test_products():
    return {"message": "Products pong"}


@router.post("/products/", response_model=ProductSchema)
def create_product(
    product: ProductSchema,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    repository = DatabaseProductRepository(db)
    use_case = ProductUseCase(repository)
    return use_case.create_product(product)


@router.get("/products/", response_model=List[ProductSchema])
def get_all_products(db: Session = Depends(get_db)):
    repository = DatabaseProductRepository(db)
    use_case = ProductUseCase(repository)
    return use_case.get_all_products()
