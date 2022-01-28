from sqlalchemy import Column, Integer, String, BigInteger, Text
from database import Base


class Holivar_unit(Base):
    __tablename__ = 'dataminer_holivar_unit'
    unit_id = Column(Integer, primary_key=True)
    key = Column(Integer, nullable=False)
    message = Column(String(250),nullable=False)
    json_data = Column(Text,default=0)
    answer_to_key = Column(Integer, default="0")
    user_id = Column(BigInteger, nullable=False)
    done = Column(Integer, default="0")
    json_data = Column(Text, default="-")
    funnel_name = Column(String(250),nullable=False)


    def __init__(self, key, message,json_data, answer_to_key, user_id, funnel_name):


        self.key = key
        self.message = message
        self.json_data = json_data
        self.answer_to_key = answer_to_key
        self.user_id = user_id
        self.done = 0
        self.funnel_name = funnel_name

    def __repr__(self):
        return f'key: {self.key}; message: {self.message}; answer_to_key: {self.answer_to_key}; user_id: {self.user_id}'