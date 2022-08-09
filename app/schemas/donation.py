from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt, validator

from app.core import DATETIME_FORMAT


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationShortDB(DonationBase):
    id: int
    create_date: datetime

    @validator("create_date")
    def create_date_validate(cls, value: datetime):
        return value.strftime(DATETIME_FORMAT)

    class Config:
        orm_mode = True


class DonationDB(DonationShortDB):
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
    user_id: int

    @validator("close_date")
    def close_date_validate(cls, value: Optional[datetime]):
        if value is None:
            return None
        return value.strftime(DATETIME_FORMAT)

    class Config:
        orm_mode = True
