from sqlalchemy import Column, Integer, String, Boolean, BigInteger, Text
from sqlalchemy.ext.declarative import declarative_base
from database import Base
import time

class Telegram_dialog(Base):
    __tablename__ = 'dataminer_telegram_dialog'

    dialog_id = Column(Integer, primary_key=True,unique=True)
    sender_id = Column(BigInteger, nullable=False)
    recipient_id = Column(BigInteger, nullable=False)
    message_text = Column(Text, default = "-")
    message_time = Column(Integer, nullable=False)

    def __init__(self,sender_id, recipient_id, message_text):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.message_text = message_text
        self.message_time = int(time.time())

    def __repr__(self):
        return f'Sender_id: {self.sender_id}; recipient_id: {self.recipient_id}; message_text: {self.message_text}'