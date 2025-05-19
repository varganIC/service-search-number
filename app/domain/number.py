import re

from pydantic import BaseModel, validator


def validate_number(v):
    if not re.fullmatch(r'89\d{9}', v):
        raise ValueError(
            "Номер телефона должен быть "
            "в формате 89000000000"
        )
    return v


class NumberBase(BaseModel):
    phone: str
    address: str


class NumberCreate(NumberBase):
    @validator('phone', pre=True)
    def validate_phone(cls, v):
        return validate_number(v)


class Number(NumberBase):
    pass
