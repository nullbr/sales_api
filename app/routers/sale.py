from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Path, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/sales",
    tags=['Sales']
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Sale])
def sales(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM sales """)
    # sales = cursor.fetchall()
    
    sales = db.query(models.Sale).all()
    
    return sales

# Path parameter
@router.get("/{sale_id}", status_code=status.HTTP_200_OK, response_model=schemas.Sale)
def get_sale(sale_id: int = Path(None, description ="The ID of the desired Sale", gt=0), db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM sales WHERE id = %s """, (str(sale_id),))
    # sale = cursor.fetchone()

    sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()

    if not sale:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"category with id: {category_id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"sale with id: {sale_id} was not found")
    

    return sale

# Post method
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Sale)
def create_sale(sale: schemas.CreateSale, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO sales (item, price, quantity) VALUES (%s, %s, %s) # RETURNING * """, (sale.item, sale.price, sale.quantity))
    # new_sale = cursor.fetchone()  
    # connection.commit()
    
    new_sale = models.Sale(**sale.dict())
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    return new_sale

# Put method
@router.put("/{sale_id}", status_code=status.HTTP_200_OK, response_model=schemas.Sale)
def update_sale(sale_id: int, sale: schemas.UpdateSale, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE sales SET item = %s, price = %s, quantity = %s WHERE id = %s RETURNING *""", (sale.item, sale.price, sale.quantity, sale_id))
    # updated_sale = cursor.fetchone()
    # connection.commit()

    sale_query = db.query(models.Sale).filter(models.Sale.id == sale_id)

    if not sale_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"sale with id: {sale_id} does not exist")

    sale_query.update(sale.dict())
    db.commit()

    return sale_query.first()

# Delete method
@router.delete("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale(sale_id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
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