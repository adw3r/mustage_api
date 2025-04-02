import datetime as dt

from pydantic import BaseModel, field_validator


class ExchangeRate(BaseModel):
    iso: int
    code: str
    name: str
    ask: float
    bid: float
    trend_ask: float
    trend_bid: float
    comment: str
    is_close: bool
    date: dt.date
    datetime: dt.datetime
    timestamp: dt.datetime

    @field_validator("date", mode="before")
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, str):
            return dt.datetime.strptime(value, "%d.%m.%Y").date()
        return value

    @field_validator("datetime", "timestamp", mode="before")
    @classmethod
    def parse_datetime(cls, value):
        if isinstance(value, str):
            return dt.datetime.strptime(value, "%d.%m.%Y %H:%M:%S")
        return value

