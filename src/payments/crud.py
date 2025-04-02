from datetime import datetime

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import models


class PaymentsBase:
    def __init__(self, session: AsyncSession):
        self.session = session



class PaymentsRead(PaymentsBase):
    async def get_by_id(self, id_: int) -> models.Payment | None:
        stmt = select(models.Payment).where(models.Payment.id == id_)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_all(self) -> list[models.Payment]:
        stmt = select(models.Payment)
        result = await self.session.execute(stmt)
        return list(result.scalars())

    async def get_with_specific_date(self, date: str | datetime):
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d").date()

        stmt = select(models.Payment).where(models.Payment.created_at == date)
        result =await self.session.execute(stmt)
        return list(result.scalars())

class PaymentsDelete(PaymentsBase):
    async def delete_with_id(self, id_: str | int) -> models.Payment:
        stmt = delete(models.Payment).where(models.Payment.id == id_).returning(models.Payment)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalar()


class PaymentsCreate(PaymentsBase):
    async def insert_one(self, item: models.Payment) -> models.Payment:
        self.session.add(item)
        await self.session.commit()
        return item


class PaymentsUpdate(PaymentsRead):
    async def update_one(self, item: models.Payment) -> models.Payment | None:
        stmt = (
            update(models.Payment)
            .where(models.Payment.id == item.id)
            .values(**item.to_dict())
            .execution_options(synchronize_session="fetch").returning(models.Payment)
        )
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalar()
