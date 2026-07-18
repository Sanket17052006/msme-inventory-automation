from fastapi import HTTPException, status

from backend.schemas.order import OrderCreate, OrderOut, OrderStatusUpdate
from backend.services.order_service import OrderService


class OrderController:
    def __init__(self, service: OrderService):
        self.service = service

    async def index(self, status_filter: str | None = None) -> list[OrderOut]:
        orders = await self.service.get_all(status_filter)
        return [OrderOut.model_validate(o) for o in orders]

    async def show(self, order_id: int) -> OrderOut:
        order = await self.service.get_by_id(order_id)
        if order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return OrderOut.model_validate(order)

    async def create(self, body: OrderCreate) -> OrderOut:
        try:
            order = await self.service.create_order(
                product_id=body.product_id,
                qty=body.qty,
                supplier_id=body.supplier_id,
            )
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        return OrderOut.model_validate(order)

    async def update_status(self, order_id: int, body: OrderStatusUpdate) -> OrderOut:
        try:
            updated = await self.service.update_status(order_id, body.status)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        if updated is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return OrderOut.model_validate(updated)
