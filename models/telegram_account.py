from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from database import Base


class Telegram_account(Base):
    __tablename__ = 'dataminer_telegram_account'

    telegram_id = Column(Integer, primary_key=True)
    telegram_user_id = Column(Integer, nullable=True, default="0")
    session_file = Column(String(17), nullable=False)
    phone_id = Column(Integer,unique=False, nullable=False)
    register_time = Column(Integer,unique=True, nullable=False, default="0")
    app_id = Column(Integer,unique=False, nullable=False, default="-")
    app_hash = Column(String(250), nullable=False, default="-")
    sdk = Column(String(10), nullable=False, default="-")
    app_version=Column(String(20), nullable=False, default="-")
    device = Column(String(20), nullable=False, default="-")
    lang_pack = Column(String(10), nullable=False, default="-")
    success_registred = Column(Boolean, unique=False, default=True)
    proxy = Column(String(250), nullable=False, default="-")
    register_process = Column(Boolean, unique=False, default=False)
    first_name=Column(String(15), nullable=False, default="-")
    last_name=Column(String(15), nullable=False, default="-")
    last_check_time=Column(Integer, nullable=False, default="0")
    deleted = Column(Boolean, unique=False, default=False)
    password = Column(Boolean, unique=False, default=False)
    password_str = Column(String(250), nullable=False)
    avatar = Column(String(250), default="-")
    username = Column(String(250), nullable=False)




    def __init__(self,data):
        self.telegram_user_id = int(data['telegram_user_id'])
        self.session_file = data['session_file']
        self.phone_id = data['phone_id']
        self.register_time = data['register_time']
        self.app_id = data['app_id']
        self.app_hash = data['app_hash']
        self.sdk = data['sdk']
        self.app_version = data['app_version']
        self.device = data['device']
        self.lang_pack = data['lang_pack']
        self.success_registred = data['success_registred']
        self.proxy = data['proxy']
        self.register_process = data['register_process']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.last_check_time = data['last_check_time']
        self.deleted = data['deleted']
        self.password = data['password']
        self.password_str = data['password_str']
        self.avatar = data['avatar']
        self.username = data['username']

    def __repr__(self):
        return f'UserName: self.username;'