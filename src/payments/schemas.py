import datetime as dt
from typing import Any

from pydantic import BaseModel, field_validator


class PaymentBase(BaseModel):
    id: Any


class PaymentCreate(BaseModel):
    created_at: dt.date
    comment: str
    amount_uah: float
    amount_usd: float | None = None
    @field_validator("created_at", mode="before")
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, str):
            return dt.datetime.strptime(value, "%d.%m.%Y").date()
        return value


class PaymentsResponse(PaymentBase):
    created_at: dt.date
    comment: str
    amount_uah: float
    amount_usd: float

class PaymentPatch(BaseModel):
    comment: str | None = None
    amount_uah: float | None = None
