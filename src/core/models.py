import datetime

from sqlalchemy import FLOAT, Date, Integer, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime.date] = mapped_column(Date)
    comment: Mapped[str] = mapped_column(String)
    amount_uah: Mapped[float] = mapped_column(FLOAT)
    amount_usd: Mapped[float] = mapped_column(FLOAT)

    def __repr__(self):
        return f"Payment({self.id=}, {self.comment=}, {self.amount_usd=}, {self.amount_uah=}, {self.created_at=})"

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "comment": self.comment,
            "amount_uah": self.amount_uah,
            "amount_usd": self.amount_usd,
        }
