from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database import Base

class Telegram_account_groups(Base):
    __tablename__ = 'dataminer_telegram_account_groups'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, nullable=False)
    chat_id = Column(BigInteger, nullable=False)

    def __init__(self, telegram_id, chat_id):
        self.telegram_id = telegram_id
        self.chat_id = chat_id


    def __repr__(self):
        return f'telegram_id: {self.telegram_id}; chat_id: {self.chat_id};'