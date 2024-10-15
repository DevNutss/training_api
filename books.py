#use http request methods
#get: read resource
#post: create resource
#put: update/replace resource
#delete: delete resource 

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

#handle open & close connection to db
def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()


class Book(BaseModel):
    #id:UUID #we can removed it cause our db gonna handles that on its own 
    title: str = Field(min_length=1) #the user must type a title of at least one char
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating:int = Field(gt=-1, lt=101) #greater than -1 = 0 et less than 101 so 100

BOOKS = []

@app.get("/") #annotation for fastapi to know it's a get request function 
#"/":empty string 
# Depends => when the function get called we want to automatically open the db and close the session
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Books).all()
    #return{"Welcome": name} #return test 


#if no db whenever the app reset the list is empty by default 
@app.post("/")
def create_book(book: Book, db: Session = Depends(get_db)):
    book_model = models.Books()
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit() #commit the model to db

    return book


#implement http exeception to catch errors that pydantic won't catch like business errors 
@app.put("/{book_id}") #put in parameter the book id 
def update_book(book_id: int, book: Book, db: Session =Depends(get_db)):

    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()
    #meaning looks thru every record until models.Books.id == book_id we are passing in
    #.first() = when found it thezn return it 

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail= f"ID {book_id} does not exist"    
        )
    
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()

    return book

            #this is called the path parameter
@app.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):

    book_model = db.query(models.Books).filter(models.Books.id == book_id).first() #make sur the db exists

    if book_model is None:
        raise HTTPException(
            status_code=404, 
            detail= f"ID {book_id} does not exist"
        )
    
    db.query(models.Books).filter(models.Books.id == book_id).delete()
    db.commit()
