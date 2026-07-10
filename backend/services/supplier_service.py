from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.supplier import Supplier


class SupplierService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Supplier]:
        pass

    async def get_by_id(self, supplier_id: int) -> Supplier | None:
        pass
