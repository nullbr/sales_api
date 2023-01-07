from .. import models, schemas, oauth2
from fastapi import FastAPI, Path, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/sales",
    tags=['Sales']
)


@router.get("/", status_code=status.HTTP_200_OK)
def sales(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, offset: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM sales """)
    # sales = cursor.fetchall()
    
    '''Group Products'''
    sales = db.query(models.Sale, func.count(models.ProductSold.sale_id).label('products')).join(models.ProductSold, models.ProductSold.sale_id == models.Sale.id, isouter=True).group_by(models.Sale.id)

    '''Filter'''
    # sales = sales.filter(models.Sale.items.contains(search)).limit(limit).offset(offset).all()
    sales = sales.limit(limit).offset(offset).all()
    
    return sales

# Path parameter
@router.get("/{sale_id}", status_code=status.HTTP_200_OK)
def get_sale(sale_id: int = Path(None, description ="The ID of the desired Sale", gt=0), db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM sales WHERE id = %s """, (str(sale_id),))
    # sale = cursor.fetchone()

    sale = db.query(models.Sale, func.count(models.ProductSold.sale_id).label('products'))\
             .join(models.ProductSold, models.ProductSold.sale_id == models.Sale.id, isouter=True)\
             .group_by(models.Sale.id).filter(models.Sale.id == sale_id).first()

    if not sale:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"category with id: {category_id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"sale with id: {sale_id} was not found")
    
    return sale

# Post method
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Sale)
def create_sale(sale: schemas.CreateSale, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO sales (item, price, quantity) VALUES (%s, %s, %s) # RETURNING * """, (sale.item, sale.price, sale.quantity))
    # new_sale = cursor.fetchone()  
    # connection.commit()
    
    new_sale = models.Sale(user_id=current_user.id, **sale.dict())
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    return new_sale

# Put method
@router.put("/{sale_id}", status_code=status.HTTP_200_OK, response_model=schemas.Sale)
def update_sale(sale_id: int, sale: schemas.UpdateSale, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE sales SET item = %s, price = %s, quantity = %s WHERE id = %s RETURNING *""", (sale.item, sale.price, sale.quantity, sale_id))
    # updated_sale = cursor.fetchone()
    # connection.commit()

    sale_query = db.query(models.Sale).filter(models.Sale.id == sale_id)
    selected_sale = sale_query.first()

    if not selected_sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sale with id: {sale_id} does not exist")
    
    if selected_sale.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"No allowed to update sale with id {sale_id}")

    sale_query.update(sale.dict(), synchronize_session=False)
    db.commit()

    return selected_sale

# Delete method
@router.delete("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale(sale_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM sales WHERE id = %s RETURNING *""", (str(sale_id),))
    # deleted_sale = cursor.fetchone()
    # connection.commit()

    sale_query = db.query(models.Sale).filter(models.Sale.id == sale_id)
    selected_sale = sale_query.first()

    if not selected_sale:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"category with id: {category_id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sale with id: {sale_id} does not exist")

    if selected_sale.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"No allowed to delete sale with id {sale_id}")
    
    sale_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)