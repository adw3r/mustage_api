import pytest

from src.exchanges.parsers import MinfinParser


@pytest.mark.asyncio
async def test_minfin_get_exchange_rate():
    minfin_instance = MinfinParser()
    response = await minfin_instance.get_exchange_rate()
    print(response.text)

    assert response.ok
    assert 'data' in response.json().keys()
