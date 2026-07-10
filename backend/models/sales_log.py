from sqlalchemy import Column, Integer, Date, ForeignKey, func
from sqlalchemy.orm import relationship

from backend.database import Base


class SalesLog(Base):
    __tablename__ = "sales_log"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    qty_sold = Column(Integer)
    sale_date = Column(Date, default=func.current_date())

    product = relationship("Product", back_populates="sales_logs")
