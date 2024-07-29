from abc import ABC, abstractmethod
from typing import List

from app.products.domain.model import Product


class ProductRepositoryInterface(ABC):
    @abstractmethod
    def create(self, product: Product) -> Product:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Product]:
        raise NotImplementedError

    @abstractmethod
    def update(self, product_id: int, product: Product) -> Product:
        raise NotImplementedError

    @abstractmethod
    def delete(self, product_id: int) -> None:
        raise NotImplementedError
