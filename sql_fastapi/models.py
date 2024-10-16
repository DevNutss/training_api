#table & columns of our books thats gonna be within the db
from sqlalchemy import Integer, Column, String
from database import Base

class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    description = Column(String)
    rating = Column(Integer)