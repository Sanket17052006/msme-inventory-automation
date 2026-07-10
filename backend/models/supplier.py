from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship

from backend.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    telegram_id = Column(String(50))
    lead_days = Column(Integer, default=5)
    price_per_unit = Column(Float)
    is_fallback = Column(Boolean, default=False)

    products = relationship("Product", back_populates="supplier")
    orders = relationship("Order", back_populates="supplier")
