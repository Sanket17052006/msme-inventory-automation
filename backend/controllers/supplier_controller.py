from backend.schemas.supplier import SupplierOut
from backend.services.supplier_service import SupplierService


class SupplierController:
    def __init__(self, service: SupplierService):
        self.service = service

    async def index(self) -> list[SupplierOut]:
        pass

    async def show(self, supplier_id: int) -> SupplierOut:
        pass
