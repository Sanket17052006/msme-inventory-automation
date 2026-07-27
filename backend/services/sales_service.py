from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.sales_log import SalesLog


class SalesService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(
        self,
        product_id: int | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[SalesLog]:
        query = select(SalesLog)
        if product_id is not None:
            query = query.where(SalesLog.product_id == product_id)
        if start_date is not None:
            query = query.where(SalesLog.sale_date >= start_date)
        if end_date is not None:
            query = query.where(SalesLog.sale_date <= end_date)
        query = query.order_by(SalesLog.sale_date.desc())
        result = await self.db.execute(query)
        return result.scalars().all()
