from http import HTTPStatus

from fastapi import HTTPException, Query

from app.domain.number import validate_number


def validate_query_phone(
    phone: str = Query(...)
) -> str:
    try:
        validate_number(phone)
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=e.args[0]
        )

    return phone
