from sqlalchemy import Boolean, Column, DateTime, Integer
from datetime import datetime

from app.core import Base


class BaseModel(Base):
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now)
    close_date = Column(DateTime)
