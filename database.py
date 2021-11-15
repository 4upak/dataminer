from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db_host = 'amnstrld.mysql.tools'
db_user = 'amnstrld_parsing'
db_password = 'Mm&6ry32+B'
db_name = 'amnstrld_parsing'
db_port = '3306'

#url = 'mysql://{0}:{1}@{2}:{3}'.format(db_user, db_password, db_host, port)
url = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}'
engine = create_engine(url,echo=True)

Session = sessionmaker(bind=engine)
Base = declarative_base()
def create_db():
    Base.metadata.create_all(engine)