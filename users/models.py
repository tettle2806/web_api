from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from core.models.base import Base

if TYPE_CHECKING:
    from core.models.post import Post
    from core.models.profile import Profile


class User(Base):
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, default=UUID(as_uuid=True), nullable=True
    )
    username: Mapped[str] = mapped_column(String(32), unique=True)
    email = mapped_column(String(255), unique=True)
    password = mapped_column(String(255))

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    profile: Mapped["Profile"] = relationship(back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username!r})"

    def __repr__(self):
        return str(self)
