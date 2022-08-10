import os
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Фонд поддержки котиков'
    description: str = 'Описание'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    log_file_path: str = os.path.join(
        Path(__file__).parent.parent.absolute(), 'log.txt'
    )

    class Config:
        env_file = '.env'


settings = Settings()
