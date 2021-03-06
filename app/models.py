from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, nullable=False)
    items = Column(String, nullable=False)
    total = Column(Integer, nullable=False)
    payment_method = Column(String, nullable=False)
    credit = Column(Boolean, server_default='False', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
