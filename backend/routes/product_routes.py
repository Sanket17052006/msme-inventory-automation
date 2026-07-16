from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.controllers.product_controller import ProductController
from backend.database import get_db
from backend.services.inventory_service import InventoryService

router = APIRouter()


def controller(db: AsyncSession = Depends(get_db)) -> ProductController:
    return ProductController(InventoryService(db))


@router.get("")
async def list_products(c: ProductController = Depends(controller)):
    return await c.showAll()


@router.get("/low-stock")
async def list_low_stock(c: ProductController = Depends(controller)):
    pass


@router.get("/summary")
async def get_summary(c: ProductController = Depends(controller)):
    pass


@router.get("/{product_id}")
async def get_product(product_id: int, c: ProductController = Depends(controller)):
    return await c.show(product_id)


@router.post("/{product_id}/simulate-sale")
async def simulate_sale(
    product_id: int,
    qty: int = Query(1, ge=1),
    c: ProductController = Depends(controller),
):
    return await c.simulate_sale(product_id, qty)
