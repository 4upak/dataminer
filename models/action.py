from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, Text
from database import Base


class Action(Base):
    __tablename__ = 'dataminer_action_to_do'
    action_id = Column(Integer, primary_key=True)
    action_name = Column(String(255), nullable=False)
    done = Column(Integer, default=0)
    comment = Column(Text, default="-")
    funnel_name = Column(String(255), nullable=False)


    def __init__(self, action_name, comment, funnel_name):
        self.action_name = action_name
        self.comment = comment
        self.funnel_name = funnel_name


    def __repr__(self):
        print(f"action_name:{self.action_name}; comment: {self.comment}; done: {self.done}")
