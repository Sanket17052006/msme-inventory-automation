import asyncio
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import async_session
from backend.models.product import Product
from backend.models.order import Order


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calc_order_qty(product: Product) -> int:
    safety_factor = 1.5
    qty = int(product.avg_daily_sales * 3 * safety_factor - product.stock)
    return max(qty, 1)


async def check_and_alert():
    async with async_session() as db:
        result = await db.execute(
            select(Product).where(Product.stock < Product.reorder_point)
        )
        low_stock = list(result.scalars().all())

        for product in low_stock:
            qty = calc_order_qty(product)
            logger.info(
                f"LOW STOCK: {product.name} ({product.stock} units) "
                f"→ reorder {qty} units"
            )
            order = Order(
                product_id=product.id,
                qty=qty,
                supplier_id=product.supplier_id,
                status="pending",
            )
            db.add(order)
        await db.commit()

        if low_stock:
            logger.info(f"Created {len(low_stock)} pending orders.")


async def main():
    logger.info("Stock monitor started — polling every 30s")
    while True:
        try:
            await check_and_alert()
        except Exception as e:
            logger.error(f"Error: {e}")
        await asyncio.sleep(30)


if __name__ == "__main__":
    asyncio.run(main())
