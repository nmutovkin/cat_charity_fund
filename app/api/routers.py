from fastapi import APIRouter

from .endpoints import charity_project_router

main_router = APIRouter()
main_router.include_router(
    charity_project_router, prefix='/charity_projects', tags=['Charity projects']
)
