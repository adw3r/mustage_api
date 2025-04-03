import starlette.status
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

import src.payments.crud
from src.payments import schemas
from src.core import models
from src.core.dependencies import get_session
from src.exchanges.interfaces import Minfin
from src.exchanges.schemas import ExchangeRate

from src.core.log import logger

router = APIRouter(prefix='/payments', tags=['Payments'])

@router.get("/")
async def get_payments(
        created_at: str = None,
        up_to_created_at: str | None = None,
        db: AsyncSession = Depends(get_session)) -> list[schemas.PaymentsResponse]:
    """

    :param up_to_created_at: date in format %d.%m.%Y
    :param created_at: created at date in format %d.%m.%Y
    :param db: internal dependence on db
    :return: list of PaymentsResponse json
    """
    crud = src.payments.crud.PaymentsRead(db)
    if not created_at:
        result = await crud.get_all()
        return result
    if created_at and not up_to_created_at:
        result = await crud.get_from_specific_date_to_today(created_at)
        return result
    if created_at and up_to_created_at:
        result = await crud.get_in_date_ranges(created_at, up_to_created_at)
        return result
    try:
        result = await crud.get_with_specific_date(created_at)
        if not result:
            return Response(status_code=starlette.status.HTTP_204_NO_CONTENT)
        return result
    except ValueError as error:
        raise HTTPException(status_code=starlette.status.HTTP_422_UNPROCESSABLE_ENTITY, detail={'error': str(error)})
    except Exception as error:
        logger.error(error)
        raise HTTPException(status_code=starlette.status.HTTP_500_INTERNAL_SERVER_ERROR, detail={'error': str(error)})


@router.post("/")
async def add_payment(payment: schemas.PaymentCreate, db: AsyncSession = Depends(get_session)) -> schemas.PaymentCreate:
    try:
        usd_rate_info: ExchangeRate = await Minfin.get_usd_exchange_rate()
        amount_usd = payment.amount_uah / usd_rate_info.ask
        schema_dump = payment.model_dump()
        schema_dump['amount_usd'] = amount_usd
        db_item = models.Payment(**schema_dump)
        crud = src.payments.crud.PaymentsCreate(db)
        result: models.Payment = await crud.insert_one(db_item)
        return result
    except Exception as error:
        logger.error(error)
        raise HTTPException(status_code=starlette.status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.delete("/{payment_id}")
async def delete_payment(payment_id: int, db: AsyncSession = Depends(get_session)):
    crud = src.payments.crud.PaymentsDelete(db)
    res = None
    try:
        res = await crud.delete_with_id(payment_id)
        if res:
            return JSONResponse(status_code=starlette.status.HTTP_200_OK,
                                content={'message': 'Payment deleted', 'payment_id': payment_id})
        else:
            return Response(status_code=starlette.status.HTTP_204_NO_CONTENT)
    except Exception as error:
        logger.error(error)
        raise HTTPException(status_code=starlette.status.HTTP_500_INTERNAL_SERVER_ERROR)
    raise HTTPException(status_code=starlette.status.HTTP_404_NOT_FOUND)


@router.patch("/{payment_id}")
async def patch_payment(payment_id: int, payment: schemas.PaymentPatch, db: AsyncSession = Depends(get_session)):
    crud = src.payments.crud.PaymentsUpdate(db)
    existing_model = await crud.get_by_id(payment_id)
    if not existing_model:
        raise HTTPException(status_code=starlette.status.HTTP_404_NOT_FOUND, detail='Payment not found')

    if payment.amount_uah:
        existing_model.amount_uah = payment.amount_uah
        usd_rate_info: ExchangeRate = await Minfin.get_usd_exchange_rate()
        amount_usd = payment.amount_uah / usd_rate_info.ask
        existing_model.amount_usd = amount_usd
    if payment.comment:
        existing_model.comment = payment.comment

    result = await crud.update_one(existing_model)

    return result
