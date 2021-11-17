from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from sqlalchemy.ext.declarative import declarative_base
from models.phone import Phone
from models.car import Car
from sqlalchemy.sql import func
from database import Base

class Autoria_item(Base):
    __tablename__ = 'dataminer_autoria_item'

    id = Column(Integer, primary_key=True)
    item_url = Column(String(250))
    item_id = Column(Integer,unique=True, nullable=False)
    tel_id = ForeignKey(Phone.phone_id)
    person_name = Column(String(20))
    price = Column(Integer, default=0)
    car_id = ForeignKey(Car.car_id)
    car_name = Column(String(150))
    km = Column(Integer,default=0)
    city = Column(String(100))
    update_date = Column(DateTime(timezone=True), onupdate=func.now())
    creation_date = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, item_url, item_id, tel_id, person_name, price, car_id, car_name, km, city, update_date, creation_date):
        self.item_url = item_url
        self.item_id = item_id
        self.tel_id = tel_id
        self.person_name = person_name
        self.price = price
        self.car_id = car_id
        self.car_name = car_name
        self.km = km
        self.city = city
        self.update_date = update_date
        self.creation_date = creation_date

    def __repr__(self):
        return f'item_url: {self.item_url};' \
               f'item_id: {self.item_id};' \
               f'tel_id: {self.tel_id};' \
               f'person_name: {self.person_name};' \
               f'price: {self.price};' \
               f'car_id: {self.car_id};' \
               f'car_name: {self.car_name};' \
               f'km: {self.km};' \
               f'city: {self.city};' \
               f'update_date: {self.update_date};' \
               f'creation_date: {self.creation_date};'