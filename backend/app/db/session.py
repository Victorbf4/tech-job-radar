from __future__ import annotations

import ssl
from typing import AsyncIterator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.settings import get_settings


class Database:
    _instance: Optional["Database"] = None

    def __new__(cls) -> "Database":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._engine = None
            cls._instance._session_factory = None
        return cls._instance

    @property
    def engine(self) -> AsyncEngine:
        if self._engine is None:
            settings = get_settings()
            conexion_args = {}

            if "localhost" not in settings.database_url:
                conexion_args["ssl"] = ssl.create_default_context()

            self._engine = create_async_engine(
                settings.database_url,
                connect_args=conexion_args,
                pool_pre_ping=True,
            )
        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        if self._session_factory is None:
            self._session_factory = async_sessionmaker(
                bind=self.engine,
                expire_on_commit=False,
                autoflush=False,
                autocommit=False,
            )
        return self._session_factory

    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self.session_factory() as session:
            yield session


db = Database()


async def get_db() -> AsyncIterator[AsyncSession]:
    async for session in db.get_session():
        yield session
