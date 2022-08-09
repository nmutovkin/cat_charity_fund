from datetime import datetime
from typing import Optional

from pydantic import (BaseModel, Extra, Field, PositiveInt, root_validator,
                      validator)

from app.core import DATETIME_FORMAT


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    full_amount: PositiveInt

    @root_validator
    def fields_cant_be_null(cls, values):
        for key in values:
            if values[key] == '' and key != 'close_date':
                raise ValueError(f'Поле {key} не может быть пустым!')
        return values

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: str = Field(None, min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    @validator("create_date")
    def create_date_validate(cls, value: datetime):
        return value.strftime(DATETIME_FORMAT)

    @validator("close_date")
    def close_date_validate(cls, value: Optional[datetime]):
        if value is None:
            return None
        return value.strftime(DATETIME_FORMAT)

    class Config:
        orm_mode = True
