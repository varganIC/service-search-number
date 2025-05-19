from http import HTTPStatus
from typing import Optional

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException
)

from app.api import common
from app.api import metadata as meta
from app.clients.redis import client
from app.domain.number import Number, NumberCreate

router = APIRouter(prefix=meta.api_prefix)
tag = "Реестр привязок адреса к номеру телефона"


@router.post(
    "/phone",
    tags=[tag],
    summary="Создать привязку номера телефона к адресу",
    description="Создание привязки адреса к указанному номеру телефона,"
                "в случае наличия номера - обновление не произойдет",
    response_model=Number,
    status_code=HTTPStatus.CREATED,
)
async def create_link_phone_address(
    item: NumberCreate = Body(...),
    redis: client.Redis = Depends(client.get_redis_instance)
):
    if await redis.client.get(item.phone):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Такой номер уже существует"
        )
    try:
        await redis.client.set(item.phone, item.address)
        result = await redis.client.get(item.phone)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Ошибка: {e}"
        )

    return Number(
        phone=item.phone,
        address=result
    )


@router.put(
    "/phone",
    tags=[tag],
    summary="Обновить адрес по номеру телефона",
    description="Обновление адреса по указанному номеру телефона,"
                "в случае отсутствия номера - обновления не произойдет",
    response_model=Number,
    status_code=HTTPStatus.CREATED
)
async def update_address_by_phone(
    item: NumberCreate = Body(...),
    redis: client.Redis = Depends(client.get_redis_instance)
):
    if not await redis.client.get(item.phone):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Такого номера не существует"
        )
    try:
        await redis.client.set(item.phone, item.address)
        result = await redis.client.get(item.phone)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Ошибка: {e}"
        )

    return Number(
        phone=item.phone,
        address=result
    )


@router.get(
    "/phone",
    tags=[tag],
    summary="Получить адрес по номеру телефона",
    description="Поиск адреса по указанному номеру телефона",
    response_model=Optional[Number],
    status_code=HTTPStatus.OK
)
async def get_address_by_phone(
    phone: str = Depends(common.validate_query_phone),
    redis: client.Redis = Depends(client.get_redis_instance)
):
    val = await redis.client.get(phone)
    if not val:
        return None

    return Number(
        phone=phone,
        address=val
    )
