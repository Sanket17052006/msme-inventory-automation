from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.controllers.analytics_controller import AnalyticsController
from backend.database import get_db
from backend.services.analytics_service import AnalyticsService

router = APIRouter()


def controller(db: AsyncSession = Depends(get_db)) -> AnalyticsController:
    return AnalyticsController(AnalyticsService(db))


@router.get("/summary")
async def get_summary(c: AnalyticsController = Depends(controller)):
    return await c.summary()
