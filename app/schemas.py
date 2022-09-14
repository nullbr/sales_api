from datetime import datetime
from pydantic import BaseModel, EmailStr
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
    user_id: int
    class Config:
        orm_mode = True

class Category(BaseModel):
    name: str
    options: list
    provider: Optional[str] = None


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

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
