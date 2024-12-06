from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column, Column

from .base import Base


class Post(Base):
    title: Mapped[String] = mapped_column(String(100), unique=False)
    body: Mapped[String] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),

    )