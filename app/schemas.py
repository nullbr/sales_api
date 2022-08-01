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

class Category(BaseModel):
    name: str
    options: list
    provider: Optional[str] = None
