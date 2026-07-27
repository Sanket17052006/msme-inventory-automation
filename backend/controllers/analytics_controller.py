from backend.services.analytics_service import AnalyticsService


class AnalyticsController:
    def __init__(self, service: AnalyticsService):
        self.service = service

    async def summary(self) -> dict:
        return await self.service.get_summary()
