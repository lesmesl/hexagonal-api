from typing import List

from app.products.domain.repository_interface import ProductRepositoryInterface
from app.products.infrastructure.dtos import ProductCreateSchema, ProductResponseSchema


class ProductUseCase:
    def __init__(self, repository: ProductRepositoryInterface):
        self.repository = repository

    def create_product(self, product: ProductCreateSchema) -> ProductCreateSchema:
        return self.repository.create(product)

    def get_all_products(self) -> List[ProductResponseSchema]:
        return self.repository.get_all()

    def update_product(
        self, product_id: int, product: ProductCreateSchema
    ) -> ProductCreateSchema:
        return self.repository.update(product_id, product)

    def delete_product(self, product_id: int) -> None:
        return self.repository.delete(product_id)
