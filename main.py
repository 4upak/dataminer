from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker

import datetime
import mysql.connector
from models.car import Car
from models.phone import Phone
from models.autoria_item import Autoria_item
from database import Base, engine

def create_db(engine):
    Base.metadata.create_all(engine)


def main():
    create_db(engine)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("work")
    main()
