import asyncio
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler

from backend.config import settings
from backend.database import async_session
from backend.models.order import Order
from backend.models.product import Product
from backend.services.supplier_service import SupplierService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PENDING_ALERTS: dict[str, int] = {}


async def send_alert(order_id: int, product_name: str, qty: int, supplier_name: str) -> str:
    chat_id = "YOUR_CHAT_ID"
    text = f"Order {qty} {product_name} from {supplier_name}?"
    keyboard = [
        [
            InlineKeyboardButton("✅ CONFIRM", callback_data=f"confirm_{order_id}"),
            InlineKeyboardButton("❌ REJECT", callback_data=f"reject_{order_id}"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    logger.info(f"Would send: {text}")
    return text


async def try_next_supplier(db, order: Order) -> str:
    fallback = await SupplierService(db).find_fallback(order.supplier_id)
    if fallback is None:
        return f"Order #{order.id} rejected. No fallback supplier available."
    product = await db.get(Product, order.product_id)
    order.supplier_id = fallback.id
    order.status = "pending"
    await db.commit()
    await db.refresh(order)
    sent = await send_alert(
        order.id,
        product.name if product else "?",
        order.qty,
        fallback.name,
        chat_id=fallback.telegram_id,
    )
    if sent:
        return (
            f"Order #{order.id}: original supplier rejected — "
            f"alerted {fallback.name} instead."
        )
    return f"Order #{order.id}: original supplier rejected — {fallback.name} is next."


async def handle_callback(update, context):
    query = update.callback_query
    await query.answer()
    action, order_id_str = query.data.split("_")
    order_id = int(order_id_str)

    async with async_session() as db:
        order = await db.get(Order, order_id)
        if not order:
            await query.edit_message_text("Order not found.")
            return

        if action == "confirm":
            order.status = "confirmed"
            await db.commit()
            await query.edit_message_text(f"Order #{order_id} confirmed!")
        elif action == "reject":
            message = await try_next_supplier(db, order)
            await query.edit_message_text(message)


async def main():
    if not settings.telegram_token:
        logger.warning("TELEGRAM_TOKEN not set. Bot not started.")
        return

    app = Application.builder().token(settings.telegram_token).build()
    app.add_handler(CallbackQueryHandler(handle_callback))
    logger.info("Telegram bot started")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
