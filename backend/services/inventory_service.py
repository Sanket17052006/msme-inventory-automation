from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.product import Product
from backend.models.sales_log import SalesLog


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
        result = await self.db.execute(select(Product).where(Product.id == product_id).with_for_update())
        product = result.scalar_one_or_none()
        if product is None:
            return None
        if product.stock < qty:
            raise ValueError(f"Insufficient stock: {product.stock} < {qty}")
        product.stock -= qty
        log = SalesLog(product_id=product_id, qty_sold=qty)
        self.db.add(log)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def get_summary(self) -> dict:
        pass
