from nis import cat
from sqlite3 import Cursor, connect
from urllib import response
from fastapi import FastAPI, Path, Response, status, HTTPException, Depends
from fastapi.params import  Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from requests import delete
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import sale, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# connecting to the database
while True:
    try:
        connection = psycopg2.connect(host='localhost', database='fastapi', user='nullbr', password='bmw123', cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("[INFO] Database connection was successfull!")
        break
    except Exception as error:
        print("Connection to the database failed.")
        print("[WARN]", error)
        time.sleep(2)

app.include_router(sale.router)
app.include_router(user.router)


@app.get("/")
def home():
    return { "Sales": "API" }


'''Working with categories'''

categories = { 1: {"name": "Cheeses", "options": ["Provolone", "Mozzarella", "Parmesan", "Cheddar"]} }

@app.get("/categories")
def all_categories():
    return {"data": categories}

# create a new item category with its name and product options
@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.Category):
    category_id = randrange(0, 10000000)
    categories[category_id] = category.dict()
    return {"data": category}

# Path parameter
@app.get("/categories/{category_id}")
def get_category(response: Response, category_id: int = Path(None, description ="The ID of the desired Category")):
    if category_id not in categories:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"category with id: {category_id} was not found"}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category with id: {category_id} was not found")
    
    return {"category": categories[category_id]}

# deleting category
# find the key in the dictionary that has required ID
# categories.pop(key)
@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int):
    if category_id not in categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category with id: {category_id} was not found")
    
    categories.pop(category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# deleting category
# find the index in the array that has required ID
# categories.pop(key)
@app.put("/categories/{category_id}", status_code=status.HTTP_202_ACCEPTED)
def update_category(category_id: int, category: schemas.Category):
    if category_id not in categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category with id: {category_id} was not found")
    
    categories[category_id] = category.dict()

    return {"message": "category updated"}