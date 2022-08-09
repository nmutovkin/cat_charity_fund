from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_full_amount_is_enough,
                                check_name_duplicate, check_project_exists,
                                check_project_is_closed,
                                check_project_is_invested)
from app.core import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud, donation_crud
from app.models import CharityProject
from app.schemas import (CharityProjectCreate, CharityProjectDB,
                         CharityProjectUpdate)
from app.services import invest

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProject:
    """Только для суперюзеров. Создает благотворительный проект"""

    await check_name_duplicate(project.name, session)

    project_fields = await invest(
        project.full_amount,
        donation_crud,
        session
    )

    new_project = await charity_project_crud.create(
        project, project_fields, session
    )
    return new_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
) -> List[CharityProject]:
    """Получает список всех проектов"""
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProject:
    """Только для суперюзеров.
       Закрытый проект нельзя редактировать,
       также нельзя установить требуемую сумму меньше уже вложенной."""

    project = await check_project_exists(
        project_id, session
    )

    check_project_is_closed(project)

    if obj_in.name is not None and obj_in.name != project.name:
        await check_name_duplicate(obj_in.name, session)

    if obj_in.full_amount is not None:
        check_full_amount_is_enough(obj_in.full_amount, project)

    project = await charity_project_crud.update(
        project, obj_in, session
    )
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProject:
    """Только для суперюзеров. Удаляет проект.
       Нельзя удалить проект, в который уже были инвестированы средства,
       его можно только закрыть."""

    project = await check_project_exists(
        project_id, session
    )

    check_project_is_invested(project)

    project = await charity_project_crud.delete(
        project, session
    )

    return project
