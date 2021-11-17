from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db_host = 'localhost'
db_user = 'root'
db_password = '201088'
db_name = 'datamining'
db_port = '3306'

Base = declarative_base()
url = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
print(url)
engine = create_engine(url, echo=True)

Session = sessionmaker(bind=engine)
Base = declarative_base()
