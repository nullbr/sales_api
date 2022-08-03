from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class SaleBase(BaseModel):
    items: str
    total: float
    payment_method: str
    credit: bool = False

class CreateSale(SaleBase):
    pass

class UpdateSale(SaleBase):
    pass

class Sale(SaleBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class Category(BaseModel):
    name: str
    options: list
    provider: Optional[str] = None
