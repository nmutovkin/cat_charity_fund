from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import charity_project_crud, donation_crud
from app.models import Donation, User
from app.schemas import DonationCreate, DonationDB, DonationShortDB
from app.services import invest

router = APIRouter()


@router.post(
    '/',
    response_model=DonationShortDB,
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
) -> Donation:

    """Сделать пожертвование."""

    donation_fields = await invest(
        donation.full_amount,
        charity_project_crud,
        session
    )

    new_donation = await donation_crud.create(
        donation, donation_fields, session, user
    )
    return new_donation


@router.get(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
) -> List[Donation]:
    """Только для суперюзеров. Получает список всех пожертвований."""

    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=List[DonationShortDB]
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Получить список моих пожертвований."""
    donations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return donations
