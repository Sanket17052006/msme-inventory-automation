import asyncio
import logging
import time

from sqlalchemy import exists, select
from sqlalchemy.orm import selectinload

from backend.database import async_session
from backend.models.product import Product
from backend.models.order import Order
from backend.services.supplier_service import SupplierService

import telegram_bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALERT_TIMEOUT_SECONDS = 180
_alert_sent_at: dict[int, float] = {}
_tried_suppliers: dict[int, set[int]] = {}


def calc_order_qty(product: Product) -> int:
    safety_factor = 1.5
    lead_days = product.supplier.lead_days if product.supplier else 3
    qty = int(product.avg_daily_sales * lead_days * safety_factor - product.stock)
    return max(qty, 1)


async def check_and_alert():
    has_pending_order = exists(
        select(Order.id).where(
            Order.product_id == Product.id,
            Order.status.in_(["pending", "confirmed"]),
        )
    )

    async with async_session() as db:
        result = await db.execute(
            select(Product)
            .options(selectinload(Product.supplier))
            .where(Product.stock < Product.reorder_point, ~has_pending_order)
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
            await db.flush()

            supplier = product.supplier
            supplier_name = supplier.name if supplier else "unknown supplier"
            try:
                sent = await telegram_bot.send_alert(
                    order.id,
                    product.name,
                    qty,
                    supplier_name,
                    chat_id=supplier.telegram_id if supplier else None,
                )
            except Exception as e:
                logger.error(
                    f"Order #{order.id}: alert to {supplier_name} failed: {e}"
                )
                sent = False
            if sent:
                _alert_sent_at[order.id] = time.monotonic()
                _tried_suppliers.setdefault(order.id, set()).add(order.supplier_id)

        await db.commit()

        if low_stock:
            logger.info(f"Created {len(low_stock)} pending orders.")


async def check_timeouts():
    async with async_session() as db:
        result = await db.execute(select(Order).where(Order.status == "pending"))
        pending = list(result.scalars().all())
        now = time.monotonic()

        for order_id in list(_alert_sent_at):
            if all(o.id != order_id for o in pending):
                del _alert_sent_at[order_id]
                _tried_suppliers.pop(order_id, None)

        for order in pending:
            sent_at = _alert_sent_at.get(order.id)
            if sent_at is None or now - sent_at < ALERT_TIMEOUT_SECONDS:
                continue

            tried = _tried_suppliers.get(order.id, {order.supplier_id})
            fallback = await SupplierService(db).find_fallback(order.supplier_id)
            if fallback is None or fallback.id in tried:
                logger.warning(
                    f"Order #{order.id}: no response in {ALERT_TIMEOUT_SECONDS}s "
                    "and no untried fallback supplier available — marking rejected"
                )
                order.status = "rejected"
                await db.commit()
                continue

            product = await db.get(Product, order.product_id)
            order.supplier_id = fallback.id
            await db.commit()
            await db.refresh(order)
            try:
                sent = await telegram_bot.send_alert(
                    order.id,
                    product.name if product else "?",
                    order.qty,
                    fallback.name,
                    chat_id=fallback.telegram_id,
                )
            except Exception as e:
                logger.error(
                    f"Order #{order.id}: alert to {fallback.name} failed: {e}"
                )
                sent = False
            if sent:
                _alert_sent_at[order.id] = now
                _tried_suppliers.setdefault(order.id, set()).add(fallback.id)
            logger.info(
                f"Order #{order.id}: no response in {ALERT_TIMEOUT_SECONDS}s — "
                f"trying {fallback.name}"
            )


async def main():
    logger.info("Stock monitor started — polling every 30s")
    while True:
        try:
            await check_and_alert()
            await check_timeouts()
        except Exception as e:
            logger.error(f"Error: {e}")
        await asyncio.sleep(30)


if __name__ == "__main__":
    asyncio.run(main())
