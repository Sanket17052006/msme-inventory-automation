from datetime import date

from pydantic import BaseModel


class SalesLogOut(BaseModel):
    id: int
    product_id: int
    qty_sold: int
    sale_date: date

    model_config = {"from_attributes": True}
