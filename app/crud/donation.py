from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import Donation, User
from app.schemas import DonationCreate


class CRUDDonation(
    CRUDBase[Donation, DonationCreate]
):

    async def get_by_user(
        self,
        session: AsyncSession,
        user: User
    ):
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
