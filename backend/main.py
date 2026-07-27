from contextlib import asynccontextmanager

from fastapi import FastAPI
from backend.database import init_db
from backend.routes.product_routes import router as product_router
from backend.routes.order_routes import router as order_router
from backend.routes.supplier_routes import router as supplier_router
from backend.routes.sales_routes import router as sales_router
from backend.routes.analytics_routes import router as analytics_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="MSME Supply Chain API", lifespan=lifespan)

app.include_router(product_router, prefix="/products", tags=["products"])
app.include_router(order_router, prefix="/orders", tags=["orders"])
app.include_router(supplier_router, prefix="/suppliers", tags=["suppliers"])
app.include_router(sales_router, prefix="/sales-log", tags=["sales-log"])
app.include_router(analytics_router, prefix="/analytics", tags=["analytics"])


@app.get("/health")
async def health():
    return {"status": "ok"}
