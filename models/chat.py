from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, Text
from database import Base


class Chat(Base):
    __tablename__ = 'dataminer_chats'
    chat_id = Column(Integer, primary_key=True)
    chat_login = Column(String(255), default='-')
    members = Column(Integer, default=0)
    moderation_status = Column(Integer, default=0)
    last_interaction = Column(BigInteger, default=0)
    active = Column(Integer, default=0)
    active_funnel = Column(String(255), default='-')


    def __init__(self, chat_login, members, moderation_status, last_interaction):
        self.chat_login = chat_login
        self.members = members
        self.moderation_status = moderation_status
        self.last_interaction = last_interaction



    def __repr__(self):
        return f'chat_login: {self.chat_login}; members: {self.members}; moderation_status: {self.moderation_status}; last_interaction: {self.last_interaction}'