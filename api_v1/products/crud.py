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
