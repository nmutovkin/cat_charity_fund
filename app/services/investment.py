from datetime import datetime
from typing import Optional, Tuple, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase

CRUDType = TypeVar('CRUDType', bound=CRUDBase)


async def invest(
    full_amount: int,
    crud: CRUDType,
    session: AsyncSession
) -> Tuple[int, bool, datetime, Optional[datetime]]:

    # get list of available donations/projects to invest in project
    objs = await crud.get_available_objs(session)
    invested_amount = 0
    fully_invested = False
    close_date = None

    if not objs:
        return invested_amount, fully_invested, close_date

    for obj in objs:
        session.add(obj)
        obj_amount = obj.full_amount - obj.invested_amount
        remained_amount = full_amount - invested_amount

        invested_in = min(obj_amount, remained_amount)
        invested_amount += invested_in

        obj.invested_amount += invested_in
        if obj.invested_amount >= obj.full_amount:
            obj.fully_invested = True
            obj.close_date = datetime.now()

        if invested_amount >= full_amount:
            fully_invested = True
            close_date = datetime.now()
            break

    return invested_amount, fully_invested, close_date
