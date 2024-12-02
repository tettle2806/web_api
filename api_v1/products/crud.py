"""
Create
Read
Update
Delete
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.horizontal_shard import set_shard_id

from core.models import Product
from sqlalchemy import select
from sqlalchemy.engine import Result
from .schemas import ProductCreate


async def get_products(session: AsyncSession) -> list[Product]:
    stnt = select(Product).order_by(Product.id)
    result: Result = await session.execute(stnt)
    products = result.scalars().all()
    return list(products)


async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def create_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    # await session.refresh(product)
    return product


async def update_product(
        session: AsyncSession,
        product: Product,
        product_update: ProductUpdate
) -> Product:
    for name, value in product_update.model_dump().items():
        setattr(product, name, value)
    await session.commit()
    return product


async def product_update_partial(
        session: AsyncSession,
        product: Product,
        product_update: ProductPartial
) -> Product:
    for name, value in product_update.model_dump(exclude_unset=True).items():
        setattr(product, name, value)
    await session.commit()
    return product