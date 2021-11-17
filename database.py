from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models.car import Car
from models.phone import Phone
from models.autoria_item import Autoria_item

def create_db(engine):
    Base.metadata.create_all(engine)

db_host = '127.0.0.1'
db_user = 'root'
db_password = '201088'
db_name = 'datamining'
db_port = '3306'

#url = 'mysql://{0}:{1}@{2}:{3}'.format(db_user, db_password, db_host, port)
url = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}'
engine = create_engine(url,echo=True)

Session = sessionmaker(bind=engine)
Base = declarative_base()
print("work")
create_db(engine)
