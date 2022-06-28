from fastapi import FastAPI

app = FastAPI()

sales = {
    1: {"item": "item1", "price": 5, "qty": 1},
    2: {"item": "item2", "price": 6, "qty": 2},
    3: {"item": "item3", "price": 7, "qty": 3},
    4: {"item": "item4", "price": 8, "qty": 4},
}

@app.get("/")
def home():
    return { "Sales": len(sales) }

@app.get("/sales/{sale_id}")
def get_sale(sale_id: int):
    return sales[sale_id]