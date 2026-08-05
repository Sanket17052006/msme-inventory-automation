from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.order import Order
from backend.models.product import Product
from backend.models.supplier import Supplier

VALID_TRANSITIONS = {
    "pending": ["confirmed", "rejected"],
    "confirmed": ["fulfilled"],
    "rejected": [],
    "fulfilled": [],
}


class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, status: str | None = None) -> list[Order]:
        query = select(Order)
        if status:
            query = query.where(Order.status == status)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, order_id: int) -> Order | None:
        result = await self.db.execute(select(Order).where(Order.id == order_id))
        return result.scalar_one_or_none()

    async def create_order(self, product_id: int, qty: int, supplier_id: int | None = None) -> Order:
        product = await self.db.execute(select(Product).where(Product.id == product_id))
        if product.scalar_one_or_none() is None:
            raise ValueError(f"Product with id {product_id} not found")
        if supplier_id is not None:
            supplier = await self.db.execute(select(Supplier).where(Supplier.id == supplier_id))
            if supplier.scalar_one_or_none() is None:
                raise ValueError(f"Supplier with id {supplier_id} not found")
        order = Order(product_id=product_id, qty=qty, supplier_id=supplier_id)
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        return order

    async def update_status(self, order_id: int, new_status: str) -> Order | None:
        result = await self.db.execute(select(Order).where(Order.id == order_id).with_for_update())
        order = result.scalar_one_or_none()
        if order is None:
            return None
        allowed = VALID_TRANSITIONS.get(order.status, [])
        if new_status not in allowed:
            raise ValueError(
                f"Invalid transition: {order.status} -> {new_status}. Allowed: {allowed}"
            )
        order.status = new_status
        if new_status == "fulfilled":
            product_result = await self.db.execute(
                select(Product)
                .where(Product.id == order.product_id)
                .with_for_update()
            )
            product = product_result.scalar_one_or_none()
            if product is None:
                raise ValueError(f"Product with id {order.product_id} not found")
            product.stock = product.stock + order.qty
        await self.db.commit()
        await self.db.refresh(order)
        return order
