from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database import Base
class Phone(Base):
    __tablename__ = 'dataminer_phone'
    phone_id = Column(Integer, primary_key=True)
    tel = Column(Integer, nullable=False)
    geo = Column(String(5), default="-")
    operator = Column(String(20), default="-")

    def __init__(self, tel: str, geo: str, operator: str):
        self.tel = tel
        self.geo = geo
        self.operator = operator

    def __repr__(self):
        return f'Tel: {self.tel}; Geo: {self.geo}; Operator: {self.operator}'