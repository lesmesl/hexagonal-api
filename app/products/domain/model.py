from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float
    in_stock: bool
    description: str = ""
