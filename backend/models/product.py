from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from backend.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    sku = Column(String(50), unique=True)
    stock = Column(Integer, default=0)
    reorder_point = Column(Integer, default=10)
    avg_daily_sales = Column(Float, default=5.0)
    price = Column(Float)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))

    supplier = relationship("Supplier", back_populates="products")
    orders = relationship("Order", back_populates="product")
    sales_logs = relationship("SalesLog", back_populates="product")
