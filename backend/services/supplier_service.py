from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.supplier import Supplier


class SupplierService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Supplier]:
        result = await self.db.execute(select(Supplier))
        return result.scalars().all()

    async def get_by_id(self, supplier_id: int) -> Supplier | None:
        result = await self.db.execute(select(Supplier).where(Supplier.id == supplier_id))
        return result.scalar_one_or_none()

    async def find_fallback(self, current_supplier_id: int) -> Supplier | None:
        result = await self.db.execute(
            select(Supplier)
            .where(Supplier.id != current_supplier_id)
            .order_by(Supplier.is_fallback.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()
