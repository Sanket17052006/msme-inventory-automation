from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.controllers.sales_controller import SalesController
from backend.database import get_db
from backend.schemas.sales_log import SalesLogOut
from backend.services.sales_service import SalesService

router = APIRouter()


def controller(db: AsyncSession = Depends(get_db)) -> SalesController:
    return SalesController(SalesService(db))


@router.get("", response_model=list[SalesLogOut])
async def list_sales_log(
    product_id: int | None = Query(None),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    c: SalesController = Depends(controller),
):
    return await c.index(
        product_id=product_id,
        start_date=start_date,
        end_date=end_date,
    )
