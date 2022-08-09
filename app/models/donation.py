from sqlalchemy import Column, ForeignKey, Integer, Text

from .base_model import BaseModel


class Donation(BaseModel):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
