from pydantic import BaseModel


class ProductOut(BaseModel):
    id: int
    name: str
    sku: str | None = None
    stock: int
    reorder_point: int
    avg_daily_sales: float
    price: float | None = None
    supplier_id: int | None = None

    model_config = {"from_attributes": True}


class ProductCreate(BaseModel):
    name: str
    sku: str | None = None
    stock: int = 0
    reorder_point: int = 10
    avg_daily_sales: float = 5.0
    price: float | None = None
    supplier_id: int | None = None
