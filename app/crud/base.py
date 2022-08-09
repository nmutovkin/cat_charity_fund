from datetime import datetime
from typing import Generic, List, Optional, Tuple, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)


class CRUDBase(
    Generic[ModelType, CreateSchemaType]
):

    def __init__(
        self,
        model: Type[ModelType]
    ) -> None:
        self.model = model

    async def create(
        self,
        obj_in: CreateSchemaType,
        obj_fields: Tuple[int, bool, datetime, Optional[datetime]],
        session: AsyncSession,
        user: Optional[User] = None
    ) -> ModelType:
        obj_in_data = obj_in.dict()

        if user is not None:
            obj_in_data['user_id'] = user.id

        invested_amount, fully_invested, close_date = obj_fields
        obj_in_data['invested_amount'] = invested_amount
        obj_in_data['fully_invested'] = fully_invested
        obj_in_data['close_date'] = close_date

        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get(
        self,
        obj_id: int,
        session: AsyncSession
    ) -> Optional[ModelType]:
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        db_obj = db_obj.scalars().first()
        return db_obj

    async def get_multi(
        self,
        session: AsyncSession
    ) -> List[ModelType]:
        db_objs = await session.execute(
            select(self.model)
        )
        return db_objs.scalars().all()

    async def get_available_objs(
        self,
        session: AsyncSession
    ) -> List[ModelType]:
        objs = await session.execute(
            select(self.model).where(
                self.model.fully_invested.is_(False)
            ).order_by(self.model.create_date)
        )

        objs = objs.scalars().all()
        return objs
