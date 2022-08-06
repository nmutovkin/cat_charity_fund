from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_full_amount_is_enough,
                                check_name_duplicate, check_project_exists,
                                check_project_is_closed,
                                check_project_is_invested)
from app.core import get_async_session
from app.crud.charity_project import (create_charity_project, delete_project,
                                      read_all_projects_from_db,
                                      update_project)
from app.models import CharityProject
from app.schemas import (CharityProjectCreate, CharityProjectDB,
                         CharityProjectUpdate)

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True
)
async def create_new_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProject:
    await check_name_duplicate(project.name, session)
    new_project = await create_charity_project(project, session)
    return new_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session)
) -> List[CharityProject]:
    all_projects = await read_all_projects_from_db(session)
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True
)
async def partially_update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProject:
    project = await check_project_exists(
        project_id, session
    )

    check_project_is_closed(project)

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    if obj_in.full_amount is not None:
        check_full_amount_is_enough(obj_in.full_amount, project)

    project = await update_project(
        project, obj_in, session
    )
    return project


@router.delete(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True
)
async def remove_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProject:
    project = await check_project_exists(
        project_id, session
    )

    check_project_is_invested(project)

    project = await delete_project(
        project, session
    )

    return project
