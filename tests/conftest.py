import asyncio
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

import config
from database import async_engine, async_session
from main import app
from src.notes.models import Base


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_db_setup_sessionmaker():
    assert config.settings.ENVIRONMENT == "PYTEST"

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(autouse=True)
async def session(test_db_setup_sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

        # TODO: Implement db split;
        # # delete all data from all tables after test
        # for name, table in Base.metadata.tables.items():
        #     await session.execute(delete(table))
        # await session.commit()


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        client.headers.update({"Host": "localhost"})
        yield client
