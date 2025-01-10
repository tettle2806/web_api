from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING

from .order_product_association import order_product_association_table
from .base import Base
from sqlalchemy import func

if TYPE_CHECKING:
    from .product import Product


class Order(Base):
    promocode: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow(),
    )
    products: Mapped[list["Product"]] = relationship(
        back_populates="orders",
        secondary=order_product_association_table,
    )
