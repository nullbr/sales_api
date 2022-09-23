from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Optional

'''Users'''
class UserBase(BaseModel):
    email: EmailStr
    password: str

class CreateUser(UserBase):
    pass

class User(BaseModel):
    id: int
    created_at: datetime
    email: str
    class Config:
        orm_mode = True

'''Auth'''
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

'''Sales'''
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
    user: User
    class Config:
        orm_mode = True

class SaleOut(SaleBase):
    Sale: Sale
    products: int
    class Config:
        orm_mode = True

'''Products'''
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    inventory: int
    on_sale_price: float
    on_sale: bool = False

class CreateProduct(ProductBase):
    pass

class UpdateProduct(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime
    user: User
    class Config:
        orm_mode = True

'''Products / Sales join'''
class ProductSold(BaseModel):
    product_id: int
    sale_id: int
    quantity: conint(ge=1)