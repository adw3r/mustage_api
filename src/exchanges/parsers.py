import curl_cffi
from curl_cffi import requests


class MinfinParser:
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,uk;q=0.7",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://minfin.com.ua/ua/currency/mb/",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0;"
        " Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    }

    async def get_exchange_rate(self) -> curl_cffi.Response:
        params = {
            "locale": "uk",
        }

        response = requests.get(
            "https://minfin.com.ua/api/currency/rates/interbank/",
            params=params,
            headers=self.headers,
        )
        return response
