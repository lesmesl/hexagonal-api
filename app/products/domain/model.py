from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    name: str
    price: float
    in_stock: bool
    description: Optional[str] = ""
