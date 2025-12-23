from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from decimal import Decimal
import uuid

from app.models.cart_items import CartItem
from app.models.cart import Cart
from app.models.order import Order 
from app.models.order_item import OrderItem
from app.models.product import Product
from app.orders.schemas import OrderOut, OrderItemOut, OrderListOut

async def place_order(
    db: AsyncSession,
    *,
    user_id: uuid.UUID,
    address_id: uuid.UUID
) -> OrderOut:

    result = await db.execute(
        select(CartItem).join(Cart).where(Cart.user_id == user_id)
    )
    cart_items = result.scalars().all()

    if not cart_items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No items in cart")

    product_ids = [item.product_id for item in cart_items]
    products_result = await db.execute(select(Product).where(Product.id.in_(product_ids)))
    products = {p.id: p for p in products_result.scalars().all()}

    total_amount = Decimal("0.00")
    order_items = []

    for item in cart_items:
        product = products.get(item.product_id)
        if not product or product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"{product.name if product else 'Product'} is out of stock"
            )
        total_amount += product.price * item.quantity
        order_items.append(
            OrderItem(
                product_id=product.id,
                product_name=product.name,
                quantity=item.quantity,
                price_at_purchase=product.price
            )
        )

    for item in cart_items:
        await db.execute(
            update(Product)
            .where(Product.id == item.product_id)
            .values(stock=Product.stock - item.quantity)
        )

    order = Order(
        user_id=user_id,
        address_id=address_id,
        total_amount=total_amount,
        items=order_items
    )
    db.add(order)

    for item in cart_items:
        await db.delete(item)

    await db.commit()

    final_result = await db.execute(
        select(Order)
        .where(Order.id == order.id)
        .options(selectinload(Order.items))
    )
    order = final_result.scalar_one()

    return OrderOut(
        id=order.id,
        total_amount=order.total_amount,
        status=order.status,
        created_at=order.created_at,
        items=[
            OrderItemOut(
                product_id=i.product_id,
                product_name=i.product_name,
                quantity=i.quantity,
                price_at_purchase=i.price_at_purchase
            ) for i in order.items
        ]
    )

async def get_all_orders(db: AsyncSession, user_id: uuid.UUID):
    result = await db.execute(
        select(Order)
        .where(Order.user_id == user_id)
        .options(selectinload(Order.items))
        .order_by(Order.created_at.desc())
    )
    orders = result.scalars().all()
    
    return [
        OrderListOut(
            id=order.id,
            total_amount=order.total_amount,
            status=order.status,
            created_at=order.created_at
        ) for order in orders
    ]


async def get_order_by_id(db:AsyncSession,user_id:uuid.UUID, order_id:uuid.UUID)->Order:
    result = await db.execute(
        select(Order)
        .where(Order.id == order_id ,Order.user_id==user_id)
        .options(selectinload(Order.items))
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail= "order not found"
        )
    return OrderOut(
            id=order.id,
            total_amount=order.total_amount,
            status=order.status,
            created_at=order.created_at,
            items=[
                OrderItemOut(
                    product_id=i.product_id,
                    product_name=i.product_name,
                    quantity=i.quantity,
                    price_at_purchase=i.price_at_purchase
                ) for i in order.items
            ]
        )       