import asyncio
import os
import random
from datetime import date, timedelta

from backend.database import async_session, init_db
from backend.models.product import Product
from backend.models.supplier import Supplier
from backend.models.sales_log import SalesLog

PRODUCTS = [
    {"name": "Steel Rod", "sku": "SR-001", "reorder_point": 5, "avg_daily_sales": 8, "price": 300},
    {"name": "PVC Pipe", "sku": "PVC-002", "reorder_point": 10, "avg_daily_sales": 6, "price": 120},
    {"name": "Brass Fitting", "sku": "BF-003", "reorder_point": 20, "avg_daily_sales": 3, "price": 450},
    {"name": "Copper Wire", "sku": "CW-004", "reorder_point": 15, "avg_daily_sales": 7, "price": 80},
    {"name": "Aluminium Sheet", "sku": "AS-005", "reorder_point": 8, "avg_daily_sales": 4, "price": 600},
    {"name": "Iron Nail (Box)", "sku": "IN-006", "reorder_point": 25, "avg_daily_sales": 12, "price": 50},
    {"name": "Wooden Plank", "sku": "WP-007", "reorder_point": 10, "avg_daily_sales": 5, "price": 200},
    {"name": "Glass Panel", "sku": "GP-008", "reorder_point": 4, "avg_daily_sales": 2, "price": 800},
    {"name": "Rubber Gasket", "sku": "RG-009", "reorder_point": 30, "avg_daily_sales": 15, "price": 25},
    {"name": "Ceramic Tile", "sku": "CT-010", "reorder_point": 12, "avg_daily_sales": 6, "price": 150},
]

DEMO_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

SUPPLIERS = [
    {"name": "Prime Traders", "telegram_id": DEMO_CHAT_ID, "lead_days": 3, "price_per_unit": 1.0, "is_fallback": False},
    {"name": "Metro Supplies", "telegram_id": DEMO_CHAT_ID, "lead_days": 5, "price_per_unit": 1.1, "is_fallback": True},
    {"name": "City Wholesale", "telegram_id": DEMO_CHAT_ID, "lead_days": 2, "price_per_unit": 1.2, "is_fallback": True},
]


async def seed():
    await init_db()
    async with async_session() as db:
        suppliers = []
        for s in SUPPLIERS:
            supplier = Supplier(**s)
            db.add(supplier)
            suppliers.append(supplier)
        await db.flush()

        products = []
        for i, p in enumerate(PRODUCTS):
            product = Product(
                name=p["name"],
                sku=p["sku"],
                stock=random.randint(3, 50),
                reorder_point=p["reorder_point"],
                avg_daily_sales=p["avg_daily_sales"],
                price=p["price"],
                supplier_id=suppliers[i % len(suppliers)].id,
            )
            db.add(product)
            products.append(product)
        await db.flush()

        today = date.today()
        for product in products:
            for days_ago in range(90):
                sale_date = today - timedelta(days=days_ago)
                qty = max(0, int(random.gauss(product.avg_daily_sales, 2)))
                if qty > 0:
                    log = SalesLog(product_id=product.id, qty_sold=qty, sale_date=sale_date)
                    db.add(log)

        await db.commit()
        print(f"Seeded {len(SUPPLIERS)} suppliers, {len(PRODUCTS)} products, and ~{len(PRODUCTS) * 90} sales records.")


if __name__ == "__main__":
    asyncio.run(seed())
