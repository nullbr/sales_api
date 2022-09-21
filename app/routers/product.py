from .. import models, schemas, oauth2
from fastapi import FastAPI, Path, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/products",
    tags=['Products']
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Product])
def all_products(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, offset: int = 0, search: Optional[str] = ""):

    products = db.query(models.Product).filter(models.Product.name.contains(search)).limit(limit).offset(offset).all()

    return products

# Path parameter
@router.get("/{product_id}", status_code=status.HTTP_200_OK, response_model=schemas.Product)
def get_product(product_id: int = Path(None, description ="The ID of the desired Product", gt=0), db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM products WHERE id = %s """, (str(product_id),))
    # product = cursor.fetchone()

    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not product:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"category with id: {category_id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product with id: {product_id} was not found")
    
    return product

# Post method
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Product)
def create_product(product: schemas.CreateProduct, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO products (item, price, quantity) VALUES (%s, %s, %s) # RETURNING * """, (product.item, product.price, product.quantity))
    # new_product = cursor.fetchone()  
    # connection.commit()
    
    new_product = models.Product(user_id=current_user.id, **product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

# Put method
@router.put("/{product_id}", status_code=status.HTTP_200_OK, response_model=schemas.Product)
def update_product(product_id: int, product: schemas.UpdateProduct, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE products SET item = %s, price = %s, quantity = %s WHERE id = %s RETURNING *""", (product.item, product.price, product.quantity, product_id))
    # updated_product = cursor.fetchone()
    # connection.commit()

    product_query = db.query(models.Product).filter(models.Product.id == product_id)
    selected_product = product_query.first()

    if not selected_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id: {product_id} does not exist")
    
    if selected_product.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"No allowed to update product with id {product_id}")

    product_query.update(product.dict(), synchronize_session=False)
    db.commit()

    return selected_product

# Delete method
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM products WHERE id = %s RETURNING *""", (str(product_id),))
    # deleted_product = cursor.fetchone()
    # connection.commit()

    product_query = db.query(models.Product).filter(models.Product.id == product_id)
    selected_product = product_query.first()

    if not selected_product:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"category with id: {category_id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id: {product_id} does not exist")

    if selected_product.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"No allowed to delete product with id {product_id}")
    
    product_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)