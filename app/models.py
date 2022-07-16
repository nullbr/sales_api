from email.policy import default
from xmlrpc.client import Boolean
from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, nullable=False)
    items = Column(String, nullable=False)
    total = Column(Integer, nullable=False)
    payment_method = Column(String, nullable=False)
    credit = Column(Boolean, default=False)
