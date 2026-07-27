from datetime import date

from fastapi import HTTPException, status

from backend.schemas.sales_log import SalesLogOut
from backend.services.sales_service import SalesService


class SalesController:
    def __init__(self, service: SalesService):
        self.service = service

    async def index(
        self,
        product_id: int | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[SalesLogOut]:
        logs = await self.service.get_all(
            product_id=product_id,
            start_date=start_date,
            end_date=end_date,
        )
        if not logs:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No sales log entries found",
            )
        return [SalesLogOut.model_validate(log) for log in logs]
