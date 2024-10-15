# we want to create & connect a database to the fastapi app and core operations
# so we don't have to handle the db everytime we reset the db 
# create the db.py file = config file to manipulate our db
# we gonna use sqlalchemy = orm = (object relation mapping) for our database
# the library gonna handle all the bts code handling records in our database

#imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args ={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#this is all we need for connection processes from our db.py to our sqlite db