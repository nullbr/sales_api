from nis import cat
from sqlite3 import Cursor, connect
from fastapi import FastAPI, Path, Response, status, HTTPException, Depends
from fastapi.params import  Body
from typing import Optional
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# connecting to the database
while True:
    try:
        connection = psycopg2.connect(host='localhost', database='fastapi', user='brunoleite', password='fastapi123', cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("[INFO] Database connection was successfull!")
        break
    except Exception as error:
        print("Connection to the database failed.")
        print("[WARN]", error)
        time.sleep(2)

sales = {
    1: {"item": "item1", "price": 5, "qty": 1},
    2: {"item": "item2", "price": 6, "qty": 2},
    3: {"item": "item3", "price": 7, "qty": 3},
    4: {"item": "item4", "price": 8, "qty": 4},
}

categories = { 1: {"name": "Cheeses", "options": ["Provolone", "Mozzarella", "Parmesan", "Cheddar"]} }

class Sale(BaseModel):
    item: str
    price: int
    quantity: int

class UpdateSale(BaseModel):
    item: Optional[str]
    price: Optional[int]
    quantity: Optional[int]

class Category(BaseModel):
    name: str
    options: list
    provider: Optional[str] = None

@app.get("/")
def home():
    return { "Sales": "API" }

@app.get("/sqlalchemy")
def test_sales(db: Session = Depends(get_db)):
    sales = db.query(models.Sale).all()
    
    return {"status": sales}

@app.get("/sales")
def sales(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM sales """)
    # sales = cursor.fetchall()
    
    sales = db.query(models.Sale).all()
    
    return { "Sales": sales }

# Query parameter
@app.get("/sales-by-price")
def get_sale(price: Optional[int] = None):
    for sale_id in sales:
        if sales[sale_id]["price"] == price:
            return sales[sale_id]
    return {"Sale": "Not found"}

# Path parameter
@app.get("/sales/{sale_id}")
def get_sale(sale_id: int = Path(None, description ="The ID of the desired Sale", gt=0)):
    cursor.execute("""SELECT * FROM sales WHERE id = %s """, (str(sale_id),))
    sale = cursor.fetchone()
    if not sale:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"category with id: {category_id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"sale with id: {sale_id} was not found")
    

    return { "Sale": sale}


# Post method
@app.post("/sales")
def create_sale(sale: Sale):
    cursor.execute("""INSERT INTO sales (item, price, quantity) VALUES (%s, %s, %s) RETURNING * """, (sale.item, sale.price, sale.quantity))
    new_sale = cursor.fetchone()
    
    connection.commit()

    return { "Sale": new_sale}

# Put method
@app.put("/update-sale/{sale_id}", status_code=status.HTTP_200_OK)
def update_sale(sale_id: int, sale: Sale):
    
    cursor.execute("""UPDATE sales SET item = %s, price = %s, quantity = %s WHERE id = %s RETURNING *""", (sale.item, sale.price, sale.quantity, sale_id))
    updated_sale = cursor.fetchone()
    connection.commit()

    if not updated_sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"sale with id: {sale_id} does not exist")

    return {"Updated Sale": updated_sale}

# Delete method
@app.delete("/delete-sale/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale(sale_id: int):
    cursor.execute("""DELETE FROM sales WHERE id = %s RETURNING *""", (str(sale_id),))
    deleted_sale = cursor.fetchone()
    connection.commit()

    if not deleted_sale:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"category with id: {category_id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"sale with id: {sale_id} does not exist")
    
    return { "Deleted Sale": deleted_sale }


'''Working with categories'''

@app.get("/categories")
def all_categories():
    return {"data": categories}

# create a new item category with its name and product options
@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(category: Category):
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
def update_category(category_id: int, category: Category):
    if category_id not in categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category with id: {category_id} was not found")
    
    categories[category_id] = category.dict()

    return {"message": "category updated"}