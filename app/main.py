from nis import cat
from sqlite3 import Cursor, connect
from fastapi import FastAPI, Path, Response, status, HTTPException, Depends
from fastapi.params import  Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from requests import delete
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

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


@app.get("/")
def home():
    return { "Sales": "API" }

@app.get("/sales", status_code=status.HTTP_200_OK)
def sales(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM sales """)
    # sales = cursor.fetchall()
    
    sales = db.query(models.Sale).all()
    
    return { "Sales": sales }

# Path parameter
@app.get("/sales/{sale_id}", status_code=status.HTTP_200_OK)
def get_sale(sale_id: int = Path(None, description ="The ID of the desired Sale", gt=0), db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM sales WHERE id = %s """, (str(sale_id),))
    # sale = cursor.fetchone()

    sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()

    if not sale:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"category with id: {category_id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"sale with id: {sale_id} was not found")
    

    return { "Sale": sale}

# Post method
@app.post("/sales", status_code=status.HTTP_201_CREATED)
def create_sale(sale: schemas.CreateSale, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO sales (item, price, quantity) VALUES (%s, %s, %s) # RETURNING * """, (sale.item, sale.price, sale.quantity))
    # new_sale = cursor.fetchone()  
    # connection.commit()

    new_sale = models.Sale(**sale.dict())
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    return { "Sale": new_sale}

# Put method
@app.put("/sales/{sale_id}", status_code=status.HTTP_200_OK)
def update_sale(sale_id: int, sale: schemas.UpdateSale, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE sales SET item = %s, price = %s, quantity = %s WHERE id = %s RETURNING *""", (sale.item, sale.price, sale.quantity, sale_id))
    # updated_sale = cursor.fetchone()
    # connection.commit()

    sale_query = db.query(models.Sale).filter(models.Sale.id == sale_id)

    if not sale_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"sale with id: {sale_id} does not exist")

    sale_query.update(sale.dict())
    db.commit()

    return {"Updated Sale": sale_query.first()}

# Delete method
@app.delete("/sales/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM sales WHERE id = %s RETURNING *""", (str(sale_id),))
    # deleted_sale = cursor.fetchone()
    # connection.commit()

    sale_query = db.query(models.Sale).filter(models.Sale.id == sale_id)

    if not sale_query.first():
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"category with id: {category_id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"sale with id: {sale_id} does not exist")
    
    sale_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


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