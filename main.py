from fastapi import FastAPI, Path
from fastapi.params import  Body
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

sales = {
    1: {"item": "item1", "price": 5, "qty": 1},
    2: {"item": "item2", "price": 6, "qty": 2},
    3: {"item": "item3", "price": 7, "qty": 3},
    4: {"item": "item4", "price": 8, "qty": 4},
}

class Sale(BaseModel):
    item: str
    price: int
    qty: int

class UpdateSale(BaseModel):
    item: Optional[str]
    price: Optional[int]
    qty: Optional[int]

@app.get("/")
def home():
    return { "Sales": len(sales) }

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

# create a new item category with its name and product options
@app.post("/create-category")
def create_category(payload: dict = Body(...)):
    print(payload)
    return {"new_category": f"name {payload['name']} options: {payload['options']}" }