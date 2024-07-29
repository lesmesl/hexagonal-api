from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductSchema(BaseModel):
    name: str
    price: float
    in_stock: bool
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)
