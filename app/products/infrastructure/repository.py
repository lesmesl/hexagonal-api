from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.exceptions import DatabaseException
from app.products.domain.repository_interface import ProductRepositoryInterface
from app.products.infrastructure.dtos import ProductSchema, ProductSchemaResponse
from app.products.infrastructure.models import ProductDTO


class DatabaseProductRepository(ProductRepositoryInterface):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create(self, product: ProductSchema) -> ProductSchema:
        try:
            product_data = product.dict(
                exclude_unset=True
            )  # Excluir campos no establecidos
            db_product = ProductDTO(**product_data)
            self.db.add(db_product)
            self.db.commit()
            self.db.refresh(db_product)
            return ProductSchema.model_validate(db_product)
        except Exception as e:
            self.db.rollback()
            raise DatabaseException(f"Error creating products. detail: {str(e)}")

    def get_all(self) -> List[ProductSchemaResponse]:
        try:
            products = self.db.query(ProductDTO).all()
            return [ProductSchemaResponse.model_validate(product) for product in products]
        except Exception as e:
            raise DatabaseException(f"Error getting user by email. detail: {str(e)}")

    def update(self, product_id: int, product: ProductSchema) -> ProductSchema:
        try:
            product_data = product.dict(exclude_unset=True)
            self.db.query(ProductDTO).filter(ProductDTO.id == product_id).update(
                product_data
            )
            self.db.commit()
            updated_product = self.db.query(ProductDTO).get(product_id)
            return ProductSchema.model_validate(updated_product)
        except Exception as e:
            self.db.rollback()
            raise DatabaseException(f"Error updating product. detail: {str(e)}")

    def delete(self, product_id: int) -> None:
        try:
            self.db.query(ProductDTO).filter(ProductDTO.id == product_id).delete()
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise DatabaseException(f"Error deleting product. detail: {str(e)}")
