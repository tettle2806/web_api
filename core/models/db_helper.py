from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from core.config import settings


class DataBaseHelper:
    def __init__(self, url: str, echo: bool = True):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.sesion_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.sesion_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        async with self.get_scoped_session() as session:
            yield session
            await session.remove()


db_helper = DataBaseHelper(
    url=settings.db_url,
    echo=settings.db_echo,
)
