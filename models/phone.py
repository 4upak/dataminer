from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Phone(Base):
    __tablename__ = 'dataminer_phone'
    phone_id = Column(Integer, primary_key=True)
    tel = Column(String, nullable=False)
    geo = Column(String, default="-")
    operator = Column(String, default="-")

    def __init__(self, tel: str, geo: str, operator: str):
        self.tel = tel
        self.geo = geo
        self.operator = operator

    def __repr__(self):
        return f'Tel: {self.tel}; Geo: {self.geo}; Operator: {self.operator}'