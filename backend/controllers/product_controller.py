from fastapi import HTTPException, status

from backend.schemas.product import ProductOut
from backend.services.inventory_service import InventoryService


class ProductController:
    def __init__(self, service: InventoryService):
        self.service = service

    async def index(self) -> list[ProductOut]:
        pass

    async def show(self, product_id: int) -> ProductOut:
        product = await self.service.get_by_id(product_id)
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return ProductOut.model_validate(product)

    async def low_stock(self) -> list[ProductOut]:
        pass

    async def simulate_sale(self, product_id: int, qty: int = 1) -> ProductOut:
        try:
            product = await self.service.reduce_stock(product_id, qty)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return ProductOut.model_validate(product)

    async def summary(self) -> dict:
        pass
