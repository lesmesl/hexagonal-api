from typing import Optional

from pydantic import BaseModel, ConfigDict, validator


class ProductSchema(BaseModel):
    name: str
    price: float
    in_stock: bool
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)

    @validator("price")
    def price_must_be_positive(cls, value):
        if value < 0:
            raise ValueError("Price must be positive")
        return value
