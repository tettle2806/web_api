from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from .base import Base

if TYPE_CHECKING:
    from .post import Post

class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)
    posts: Mapped[List["Post"]] = relationship(back_populates="user")
