from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core import Base


class BaseModel(Base):
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False)
    fully_invested = Column(Boolean, nullable=False)
    create_date = Column(DateTime, nullable=False)
    close_date = Column(DateTime)
