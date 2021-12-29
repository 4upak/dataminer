from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database import Base
import phonenumbers
from phonenumbers.phonenumberutil import region_code_for_country_code
from phonenumbers.phonenumberutil import region_code_for_number
from phonenumbers import carrier

class Task(Base):
    __tablename__ = 'dataminer_telegram_task'
    task_id = Column(Integer, primary_key=True)
    type = Column(String(255), nullable=False)
    sender_id = Column(BigInteger, nullable=False)
    receipient_id = Column(BigInteger, nullable=False)
    data = Column(Text, nullable=False)
    delay_after = Column(Integer, default=0)
    delay_before = Column(Integer, default=0)
    done = Column(Integer, default=0)


    def __init__(self, type,sender_id, receipient_id, data):
        self.type = type
        self.sender_id = sender_id
        self.receipient_id = receipient_id
        self.data = data


    def __repr__(self):
        return f'type: {self.type}; sender_id: {self.sender_id}; receipient_id: {self.receipient_id}; data: {self.data};'