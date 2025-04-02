import curl_cffi

from src.exchanges import parsers, schemas


class Minfin:
    parser: parsers.MinfinParser = parsers.MinfinParser()

    @classmethod
    async def get_usd_exchange_rate(cls) -> schemas.ExchangeRate:
        response: curl_cffi.Response = await cls.parser.get_exchange_rate()

        response_json = response.json()["data"]["USD"][0]
        result = schemas.ExchangeRate.model_validate(response_json)
        return result
