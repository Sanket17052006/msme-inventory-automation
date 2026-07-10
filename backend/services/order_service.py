from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.order import Order


class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, status: str | None = None) -> list[Order]:
        pass

    async def get_by_id(self, order_id: int) -> Order | None:
        pass

    async def create_order(self, product_id: int, qty: int, supplier_id: int | None = None) -> Order:
        pass

    async def update_status(self, order_id: int, status: str) -> Order | None:
        pass
