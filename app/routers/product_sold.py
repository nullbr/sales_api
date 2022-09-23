from .. import models, schemas, oauth2
from fastapi import FastAPI, Path, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/product_sold",
    tags=['ProductSold']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def sold(product_sold: schemas.ProductSold, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    '''Adding product to sale'''

    product = db.query(models.Product).filter(models.Product.id == product_sold.product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product_sold.product_id} does not exist.")

    sale = db.query(models.Sale).filter(models.Sale.id == product_sold.sale_id).first()

    if not sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sale with id {product_sold.sale_id} does not exist.")

    product_sold_query = db.query(models.ProductSold).filter(models.ProductSold.sale_id == product_sold.sale_id, models.ProductSold.product_id == product_sold.product_id)
    already_sold = product_sold_query.first()

    if already_sold:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Product {product_sold.product_id} is already in Sale {product_sold.sale_id}.")
    
    
    if product and product.inventory < product_sold.quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
        detail=f"Quantity in inventory is {product.inventory}. Cannot puchase more items than what is available.")

    add_product_to_sale = models.ProductSold(sale_id = product_sold.sale_id, product_id = product_sold.product_id, quantity = product_sold.quantity)
    db.add(add_product_to_sale)
    db.commit()

    return {"messages": "Successfuly added Product to Sale"}