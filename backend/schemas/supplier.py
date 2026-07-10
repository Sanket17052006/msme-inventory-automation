from pydantic import BaseModel


class SupplierOut(BaseModel):
    id: int
    name: str
    telegram_id: str | None = None
    lead_days: int
    price_per_unit: float | None = None
    is_fallback: bool = False

    model_config = {"from_attributes": True}


class SupplierCreate(BaseModel):
    name: str
    telegram_id: str | None = None
    lead_days: int = 5
    price_per_unit: float | None = None
    is_fallback: bool = False
