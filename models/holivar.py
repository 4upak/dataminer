from sqlalchemy import Column, Integer, String
from database import Base


class Holivar_unit(Base):
    __tablename__ = 'dataminer_holivar_unit'
    unit_id = Column(Integer, primary_key=True)
    key = Column(Integer, nullable=False)
    message = Column(String(250),nullable=False)
    answer_to_key = Column(Integer, default="0")
    user_id = Column(Integer, nullable=False)


    def __init__(self, key, message, answer_to_key, user_id):


        self.key = key
        self.message = message
        self.answer_to_key = answer_to_key
        self.user_id = user_id

    def __repr__(self):
        return f'key: {self.key}; message: {self.message}; answer_to_key: {self.answer_to_key}; user_id: {self.user_id}'