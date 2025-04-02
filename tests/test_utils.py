import pytest

from src.exchanges.interfaces import Minfin

from src.exchanges.schemas import ExchangeRate


@pytest.mark.asyncio
async def test_get_exchange_rate():
    rate: ExchangeRate = await Minfin.get_usd_exchange_rate()
    print(rate.model_dump())
    assert ExchangeRate.model_validate(rate)
