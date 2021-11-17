from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from database import Base


class Car(Base):
    __tablename__ = 'dataminer_car'
    car_id = Column(Integer, primary_key=True)
    vin = Column(String(17), unique=True, nullable=False)
    name = Column(String(250))
    regnum = Column(String(15), nullable=False)

    def __init__(self, vin: str, name: str, regnum: str):
        self.vin = vin
        self.name = name
        self.regnum = regnum

    def __repr__(self):
        return f'Name: {self.name}; Vin: {self.vin}; Regnum: {self.regnum}'

