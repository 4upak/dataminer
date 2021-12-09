from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from database import Base


class Telegram_account(Base):
    __tablename__ = 'dataminer_telegram_account'

    telegram_id = Column(Integer, primary_key=True)
    telegram_user_id = Column(Integer, nullable=False)
    session_file = Column(String(17), nullable=False)
    phone_id = Column(Integer,unique=True, nullable=False)
    register_time = Column(Integer,unique=True, nullable=False, default="0")
    app_id = Column(Integer,unique=False, nullable=False, default="-")
    app_hash = Column(String(250), nullable=False, default="-")
    sdk = Column(String(10), nullable=False, default="-")
    app_version=Column(String(10), nullable=False, default="-")
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
    password_str= Column(String(250), nullable=False)
    avatar = Column(String(250), default="-")
    username = Column(String(250), nullable=False)




    def __init__(self,data):
        self.telegram_user_id = data['telegram_user_id']
        self.session_file = data['session_file']
        self.phone_id = data['session_file']
        self.register_time = data['session_file']
        self.app_id = data['session_file']
        self.app_hash = data['session_file']
        self.sdk = data['session_file']
        self.app_version = data['session_file']
        self.device = data['session_file']
        self.lang_pack = data['session_file']
        self.success_registred = data['session_file']
        self.proxy = data['session_file']
        self.register_process = data['session_file']
        self.first_name = data['session_file']
        self.last_name = data['session_file']
        self.last_check_time = data['session_file']
        self.deleted = data['session_file']
        self.password = data['session_file']
        self.password_str = data['session_file']
        self.avatar = data['session_file']
        self.username = data['session_file']

    def __repr__(self):
        return f'UserName: self.username;'