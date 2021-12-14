from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database import Base
import phonenumbers
from phonenumbers.phonenumberutil import region_code_for_country_code
from phonenumbers.phonenumberutil import region_code_for_number
from phonenumbers import carrier

class Proxy(Base):
    __tablename__ = 'dataminer_proxy'
    proxy_id = Column(Integer, primary_key=True)
    type = Column(String(10), nullable=False)
    host = Column(String(20), nullable=False, unique=True)
    port = Column(Integer, nullable=False)
    login = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False)


    def __init__(self, proxy_string):
        proxy_data = proxy_string.split(':')
        self.type = proxy_data[0].strip()
        self.host = proxy_data[1].strip()
        self.port = proxy_data[2].strip()
        self.login = proxy_data[3].strip()
        self.password = proxy_data[4].strip()

    def __repr__(self):
        return f'type: {self.type}; host: {self.host}; port: {self.port}; Login: {self.password}; Login: {self.password};'