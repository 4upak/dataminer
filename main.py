from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker
Base = declarative_base()
import datetime

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


db_host = '127.0.0.1'
db_user = 'root'
db_password = '201088'
db_name = 'datamining'
db_port = '3306'

def create_db(engine):
    Base.metadata.create_all(engine)


def main():
    Base = declarative_base()
    url = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}'
    engine = create_engine(url, echo=True)
    create_db(engine)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("work")
    main()
