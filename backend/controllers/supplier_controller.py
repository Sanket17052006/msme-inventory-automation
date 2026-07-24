from fastapi import HTTPException, status

from backend.schemas.supplier import SupplierOut
from backend.services.supplier_service import SupplierService


class SupplierController:
    def __init__(self, service: SupplierService):
        self.service = service

    async def index(self) -> list[SupplierOut]:
        suppliers = await self.service.get_all()
        return [SupplierOut.model_validate(s) for s in suppliers]

    async def show(self, supplier_id: int) -> SupplierOut:
        supplier = await self.service.get_by_id(supplier_id)
        if supplier is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
        return SupplierOut.model_validate(supplier)
