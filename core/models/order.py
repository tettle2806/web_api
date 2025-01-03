from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .base import Base
from sqlalchemy import func

class Order(Base):
    promocode: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow()
    )
    
    