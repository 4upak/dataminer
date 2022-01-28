from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, Text
from database import Base


class Funnel_unit(Base):
    __tablename__ = 'dataminer_funnel_unit'
    unit_id = Column(Integer, primary_key=True)
    index_id = Column(Integer, nullable=False)
    text_message = Column(Text, default='-')
    json_data = Column(Text, default='-')
    answer_to = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    funnel_name = Column(String(255), default='-')
    delay_before = Column(Integer, nullable=False)
    delay_after = Column(Integer, nullable=False)



    def __init__(self, index_id, text_message,json_data,answer_to, user_id, funnel_name, delay_before, delay_after):

        self.index_id = index_id
        self.text_message = text_message
        self.json_data = json_data
        self.answer_to = answer_to
        self.user_id = user_id
        self.funnel_name = funnel_name
        self.delay_before = delay_before
        self.delay_after = delay_after




    def __repr__(self):
        return f'unit_id: {self.unit_id}; index_id: {self.index_id}; text_message: {self.text_message}; json_data: {self.json_data}; answer_to: {self.answer_to}; user_id: {self.user_id}; funnel_name: {self.funnel_name}'