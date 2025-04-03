import datetime

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.core import models
from src.core.config import DB_URI
from src.payments import crud


@pytest_asyncio.fixture(scope='function')
async def async_session():
    async_session_maker = async_sessionmaker(
        create_async_engine(url=DB_URI), expire_on_commit=False, class_=AsyncSession
    )
    async with async_session_maker() as session:
        yield session


@pytest.mark.asyncio
async def test_crud_get_all(async_session):
    result = await crud.PaymentsRead(async_session).get_all()
    print(result)
    assert result is not None
    assert isinstance(result[0], models.Payment)


@pytest.mark.asyncio
async def test_get_with_specific_date(async_session):
    result = await crud.PaymentsRead(async_session).get_with_specific_date('03.04.2025')
    print(result)
    assert result is not None
    assert isinstance(result[0], models.Payment)
    assert result[0].id is not None

@pytest.mark.asyncio
async def test_get_date_ranges(async_session):
    result = await crud.PaymentsRead(async_session).get_in_date_ranges('01.04.2025', '03.04.2025')
    print(result)
    assert result is not None

@pytest.mark.asyncio
async def test_delete(async_session):
    id_ = 2
    result = await crud.PaymentsDelete(async_session).delete_with_id(id_)
    print(result)
    assert result is not None


@pytest.mark.asyncio
async def test_insert(async_session):
    model = models.Payment(
        id=2, created_at=datetime.date(2025, 4, 1), comment='test', amount_uah=1000.0,
        amount_usd=23.3
    )
    result = await crud.PaymentsCreate(async_session).insert_one(model)
    print(result)
    assert result is not None



@pytest.mark.asyncio
async def test_update(async_session):
    item = models.Payment(
        id=3, created_at=datetime.date(2025, 4, 1), comment='updated', amount_uah=1000.0,
        amount_usd=23.3
    )
    result = await crud.PaymentsUpdate(async_session).update_one(item)
    print(result)
