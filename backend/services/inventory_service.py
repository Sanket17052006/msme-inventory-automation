from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.product import Product


class InventoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Product]:
        pass

    async def get_by_id(self, product_id: int) -> Product | None:
        pass

    async def get_low_stock(self) -> list[Product]:
        pass

    async def reduce_stock(self, product_id: int, qty: int = 1) -> Product | None:
        pass

    async def get_summary(self) -> dict:
        pass
