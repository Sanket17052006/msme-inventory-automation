from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.order import Order
from backend.models.product import Product


class AnalyticsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_summary(self) -> dict:
        total_products = await self.db.execute(select(func.count(Product.id)))
        low_stock_count = await self.db.execute(
            select(func.count(Product.id)).where(Product.stock < Product.reorder_point)
        )
        total_stock = await self.db.execute(select(func.coalesce(func.sum(Product.stock), 0)))
        total_orders = await self.db.execute(select(func.count(Order.id)))
        pending_orders = await self.db.execute(
            select(func.count(Order.id)).where(Order.status == "pending")
        )
        return {
            "total_products": total_products.scalar(),
            "low_stock_count": low_stock_count.scalar(),
            "total_stock": total_stock.scalar(),
            "total_orders": total_orders.scalar(),
            "pending_orders": pending_orders.scalar(),
        }
