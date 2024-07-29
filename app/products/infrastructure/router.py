from typing import List

from fastapi import APIRouter, Depends, Path, Security, status
from sqlalchemy.orm import Session

from app.config.config import settings
from app.config.database import get_db
from app.config.security import oauth2_scheme
from app.products.application.use_cases import ProductUseCase
from app.products.infrastructure.dtos import ProductCreateSchema, ProductResponseSchema
from app.products.infrastructure.repository import DatabaseProductRepository

router = APIRouter(tags=["Products"])


@router.post(
    settings.REGISTER_PRODUCTS_ROUTE,
    response_model=ProductCreateSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(oauth2_scheme)],
    summary="Crear un nuevo producto",
    description="Permite crear un nuevo producto en la base de datos, siempre y cuando el usuario esté autenticado mediante OAuth2. Retorna el producto creado.",
)
def create_product(
    product: ProductCreateSchema,
    db: Session = Depends(get_db),
):
    repository = DatabaseProductRepository(db)
    use_case = ProductUseCase(repository)
    return use_case.create_product(product)


@router.get(
    settings.GET_PRODUCTS_ROUTE,
    response_model=List[ProductResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Obtener todos los productos",
    description="Permite obtener todos los productos almacenados en la base de datos. Retorna una lista de productos.",
)
def get_all_products(db: Session = Depends(get_db)):
    repository = DatabaseProductRepository(db)
    use_case = ProductUseCase(repository)
    return use_case.get_all_products()


@router.put(
    settings.UPDATE_PRODUCTS_ROUTE,
    response_model=ProductCreateSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(oauth2_scheme)],
    summary="Actualizar un producto",
    description="Permite actualizar un producto almacenado en la base de datos usando el ID del producto. Retorna el producto actualizado.",
)
def update_product(
    product: ProductCreateSchema,
    product_id: int = Path(ge=1),
    db: Session = Depends(get_db),
):
    repository = DatabaseProductRepository(db)
    use_case = ProductUseCase(repository)
    return use_case.update_product(product_id, product)


@router.delete(
    settings.DELETE_PRODUCTS_ROUTE,
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(oauth2_scheme)],
    summary="Eliminar un producto",
    description="Permite eliminar un producto almacenado en la base de datos usando el ID del producto. Retorna un código de estado 204 si la eliminación es exitosa.",
)
def delete_product(product_id: int = Path(ge=1), db: Session = Depends(get_db)):
    repository = DatabaseProductRepository(db)
    use_case = ProductUseCase(repository)
    return use_case.delete_product(product_id)
