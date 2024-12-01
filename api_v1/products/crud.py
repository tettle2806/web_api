"""
Create
Read
Update
Delete
"""

from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Product
from sqlalchemy import select
from sqlalchemy.engine import Result


async def get_products(session: AsyncSession) -> list[Product]:
    stnt = select(Product).order_by(Product.id)
    result: Result = await session.execute(stnt)
    products = []
    return products

async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def create_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()