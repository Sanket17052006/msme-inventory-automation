from fastapi import HTTPException, status

from backend.schemas.product import ProductOut
from backend.services.inventory_service import InventoryService


class ProductController:
    def __init__(self, service: InventoryService):
        self.service = service

    async def index(self) -> list[ProductOut]:
        pass

    async def show(self, product_id: int) -> ProductOut:
        pass

    async def low_stock(self) -> list[ProductOut]:
        pass

    async def simulate_sale(self, product_id: int, qty: int = 1) -> ProductOut:
        pass

    async def summary(self) -> dict:
        pass
