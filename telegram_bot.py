import asyncio
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler

from backend.config import settings
from backend.database import async_session
from backend.models.order import Order

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PENDING_ALERTS: dict[str, int] = {}

_application: Application | None = None


async def handle_start(update, context):
    await update.message.reply_text("MSME stock alert bot ready. Alerts will arrive here.")


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
            await query.edit_message_text(f"Order #{order_id} confirmed!")
        elif action == "reject":
            order.status = "rejected"
            await query.edit_message_text(f"Order #{order_id} rejected.")
        await db.commit()


def get_application() -> Application:
    global _application
    if _application is None:
        _application = Application.builder().token(settings.telegram_token).build()
        _application.add_handler(CommandHandler("start", handle_start))
        _application.add_handler(CallbackQueryHandler(handle_callback))
    return _application


async def send_alert(
    order_id: int,
    product_name: str,
    qty: int,
    supplier_name: str,
    chat_id: str | None = None,
) -> bool:
    target = chat_id or settings.telegram_chat_id
    if not target:
        logger.warning(
            f"Order #{order_id}: no chat_id configured (supplier telegram_id or "
            "TELEGRAM_CHAT_ID) — alert not sent"
        )
        return False

    text = f"Order {qty} {product_name} from {supplier_name}?"
    keyboard = [
        [
            InlineKeyboardButton("✅ CONFIRM", callback_data=f"confirm_{order_id}"),
            InlineKeyboardButton("❌ REJECT", callback_data=f"reject_{order_id}"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if not settings.telegram_token:
        logger.info(f"[dry-run] Would send to {target}: {text}")
        return False

    app = get_application()
    await app.bot.send_message(chat_id=target, text=text, reply_markup=reply_markup)
    logger.info(f"Alert sent for order #{order_id} to {target}")
    return True


async def main():
    if not settings.telegram_token:
        logger.warning("TELEGRAM_TOKEN not set. Bot not started.")
        return

    app = get_application()
    logger.info("Telegram bot started")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
