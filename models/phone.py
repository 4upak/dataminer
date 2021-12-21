from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database import Base
import phonenumbers
from phonenumbers.phonenumberutil import region_code_for_country_code
from phonenumbers.phonenumberutil import region_code_for_number
from phonenumbers import carrier

class Phone(Base):
    __tablename__ = 'dataminer_phone'
    phone_id = Column(Integer, primary_key=True)
    tel = Column(String(15), nullable=False, unique=True)
    geo = Column(String(5), default="-")
    operator = Column(String(20), default="-")
    telegram_id = Column(Integer, default=0)
    telegram_checked = Column(Integer, default=0)

    def __init__(self, tel):
        phone = '+' + str(tel)
        pn = phonenumbers.parse(phone)
        geo = region_code_for_number(pn)
        operator = carrier.name_for_number(pn, geo)

        self.tel = tel
        self.geo = geo
        self.operator = operator
        self.telegram_id = 0

    def __repr__(self):
        return f'Tel_id: {self.phone_id}; Tel: {self.tel}; Geo: {self.geo}; Operator: {self.operator}'