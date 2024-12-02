from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):

    name: str
    description: str
    price: float


class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductPartial(ProductBase):
    name :str = None
    description: str = None
    price: float = None

class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
