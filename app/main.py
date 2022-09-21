from itertools import product
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import sale, user, auth, product

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(sale.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(product.router)


@app.get("/")
def home():
    return { "Sales": "API" }