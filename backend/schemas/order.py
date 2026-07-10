from datetime import datetime

from pydantic import BaseModel


class OrderOut(BaseModel):
    id: int
    product_id: int
    qty: int
    status: str
    supplier_id: int | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class OrderCreate(BaseModel):
    product_id: int
    qty: int
    supplier_id: int | None = None


class OrderStatusUpdate(BaseModel):
    status: str
