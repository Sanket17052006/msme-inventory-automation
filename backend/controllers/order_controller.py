from backend.schemas.order import OrderCreate, OrderOut, OrderStatusUpdate
from backend.services.order_service import OrderService


class OrderController:
    def __init__(self, service: OrderService):
        self.service = service

    async def index(self, status_filter: str | None = None) -> list[OrderOut]:
        pass

    async def show(self, order_id: int) -> OrderOut:
        pass

    async def create(self, body: OrderCreate) -> OrderOut:
        pass

    async def update_status(self, order_id: int, body: OrderStatusUpdate) -> OrderOut:
        pass
