from pydantic import BaseModel


class ProductBase(BaseModel):

    name: str
    description: str
    price: float


class ProductCreate(BaseModel):
    pass


class Product(ProductBase):
    id: int
