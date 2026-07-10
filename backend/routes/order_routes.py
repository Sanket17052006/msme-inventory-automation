from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.controllers.order_controller import OrderController
from backend.database import get_db
from backend.schemas.order import OrderCreate, OrderStatusUpdate
from backend.services.order_service import OrderService

router = APIRouter()


def controller(db: AsyncSession = Depends(get_db)) -> OrderController:
    return OrderController(OrderService(db))


@router.get("")
async def list_orders(
    status: str | None = Query(None),
    c: OrderController = Depends(controller),
):
    pass


@router.get("/{order_id}")
async def get_order(order_id: int, c: OrderController = Depends(controller)):
    pass


@router.post("", status_code=201)
async def create_order(body: OrderCreate, c: OrderController = Depends(controller)):
    pass


@router.patch("/{order_id}/status")
async def update_order_status(
    order_id: int,
    body: OrderStatusUpdate,
    c: OrderController = Depends(controller),
):
    pass
