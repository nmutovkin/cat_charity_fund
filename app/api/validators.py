from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    project = await charity_project_crud.get(
        project_id, session
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )

    return project


def check_project_is_closed(
    project: CharityProject,
) -> None:
    if project.fully_invested is True:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )


def check_full_amount_is_enough(
    new_full_amount: int,
    project: CharityProject
) -> None:
    if new_full_amount < project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail='Новая требуемая сумма меньше уже вложенной!'
        )


def check_project_is_invested(
    project: CharityProject
) -> None:
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
