from sqlalchemy import Boolean, Column, Float, Integer, String

from app.config.database import Base


class ProductDTO(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    in_stock = Column(Boolean, default=True)
    description = Column(String, nullable=True)
