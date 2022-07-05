from nis import cat
from fastapi import FastAPI, Path, Response, status, HTTPException
from fastapi.params import  Body
from typing import Optional
from pydantic import BaseModel
from random import randrange

app = FastAPI()

sales = {
    1: {"item": "item1", "price": 5, "qty": 1},
    2: {"item": "item2", "price": 6, "qty": 2},
    3: {"item": "item3", "price": 7, "qty": 3},
    4: {"item": "item4", "price": 8, "qty": 4},
}

categories = { 1: {"name": "Cheeses", "options": ["Provolone", "Mozzarella", "Parmesan", "Cheddar", ""]} }

class Sale(BaseModel):
    item: str
    price: int
    qty: int

class UpdateSale(BaseModel):
    item: Optional[str]
    price: Optional[int]
    qty: Optional[int]

class Category(BaseModel):
    name: str
    options: list
    provider: Optional[str] = None

@app.get("/")
def home():
    return { "Sales": len(sales) }

@app.get("/sales")
def sales():
    return { "Sales": sales }

# Path parameter
@app.get("/sales/{sale_id}")
def get_sale(sale_id: int = Path(None, description ="The ID of the desired Sale", gt=0, lt=5)):
    return sales[sale_id]

# Query parameter
@app.get("/sale-by-price")
def get_sale(price: Optional[int] = None):
    for sale_id in sales:
        if sales[sale_id]["price"] == price:
            return sales[sale_id]
    return {"Sale": "Not found"}

# Post method
@app.post("/create-sale/{sale_id}")
def create_sale(sale_id: int, sale: Sale):
    if sale_id in sales:
        return {"Error", "Sale already exists"}

    sales[sale_id] = sale
    return sales[sale_id]

# Put method
@app.put("/update-sale/{sale_id}")
def update_sale(sale_id: int, sale: UpdateSale):
    if sale_id not in sales:
        return {"Error", "Sale not found"}

    if sale.item != None:
        sales[sale_id].item = sale.item

    if sale.price != None:
        sales[sale_id].price = sale.price
    
    if sale.price != None:
        sales[sale_id].qty = sale.qty

    return sales[sale_id]

# Delete method
@app.delete("/delete-sale/{sale_id}")
def delete_sale(sale_id: int):
    if sale_id not in sales:
        return {"Error", "Sale not found"}

    del sales[sale_id]
    return {"Message": "Sale deleted successfully"}


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

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"category with id: {category_id} was not found")
    
    return {"category": categories[category_id]}

# deleting category
# find the index in the array that has required ID
# categories.pop(key)
@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int):
    if category_id not in categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"category with id: {category_id} was not found")
    
    categories.pop(category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
