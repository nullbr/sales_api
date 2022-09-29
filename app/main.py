from itertools import product
from fastapi import FastAPI
from . import models
from .routers import sale, user, auth, product, product_sold

# from .database import engine
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(sale.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(product_sold.router)


@app.get("/")
def home():
    return { "Sales": "API" }