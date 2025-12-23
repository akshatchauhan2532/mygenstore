from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update
from sqlalchemy.orm import selectinload
from uuid import UUID
from app.models.cart import Cart
from app.models.product import Product
from app.models.cart_items import CartItem
from app.cart.schemas import AddToCartIn, CartOut
from fastapi import HTTPException, status


async def get_cart_with_items(db:AsyncSession,cart_id:UUID)->Cart:
    stmt=(
        select(Cart)
        .where(Cart.id == cart_id)
        .options(selectinload(Cart.items))
    )
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_cart_by_user_id(db: AsyncSession, user_id: UUID) -> Cart:
    stmt = select(Cart).where(Cart.user_id == user_id).options(selectinload(Cart.items))
    result = await db.execute(stmt)
    cart = result.scalars().first()
    if not cart:
        cart = await get_or_create_cart(db, user_id)
    return cart


async def get_or_create_cart(db: AsyncSession, user_id: UUID) -> Cart:
    stmt = select(Cart).where(Cart.user_id == user_id)
    result = await db.execute(stmt)
    cart = result.scalars().first()

    if cart:
        return cart

    new_cart = Cart(user_id=user_id)
    db.add(new_cart)
    await db.commit()
    await db.refresh(new_cart)
    return new_cart

async def add_item_to_cart(db: AsyncSession, user_id: UUID, product_id: UUID, quantity: int = 1):
    if quantity < 1:
        raise HTTPException(status_code=400, detail="Quantity must be at least 1")
    
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.stock < quantity:
        raise HTTPException(status_code=400, detail=f"Only {product.stock_quantity} in stock")

    cart = await get_or_create_cart(db, user_id)

    stmt = select(CartItem).where(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id
    )
    result = await db.execute(stmt)
    cart_item = result.scalars().first()

    if cart_item:
        if (cart_item.quantity + quantity) > product.stock_quantity:
            raise HTTPException(status_code=400, detail="Total quantity exceeds stock")
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product.id,
            quantity=quantity,
            price_at_add=product.price
        )
        db.add(cart_item)

    await db.commit()
    return await get_cart_with_items(db, cart.id)

async def delete_item_from_cart(db:AsyncSession,product_id:UUID,user_id:UUID):
    cart = await get_or_create_cart(db, user_id)
    cart_id = cart.id
    stmt = select(CartItem).where(
        CartItem.cart_id == cart_id,
        CartItem.product_id == product_id
    )
    result = await db.execute(stmt)
    cart_item = result.scalars().first()

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )

    await db.delete(cart_item)
    await db.commit()
    return await get_cart_with_items(db, cart_id)

async def increment_by_one(db: AsyncSession, product_id: UUID, user_id: UUID):
    cart = await get_or_create_cart(db, user_id)
    
    stmt = (
        select(CartItem, Product.stock)
        .join(Product, CartItem.product_id == Product.id)
        .where(CartItem.cart_id == cart.id, CartItem.product_id == product_id)
    )
    result = await db.execute(stmt)
    data = result.first()

    if not data:
        raise HTTPException(status_code=404, detail="Item not found")
    
    cart_item, stock_qty = data

    if cart_item.quantity + 1 > stock_qty:
        raise HTTPException(status_code=400, detail="Exceeds available stock")

    cart_item.quantity += 1
    await db.commit()
    return await get_cart_with_items(db, cart.id)

async def decrement_by_one(db: AsyncSession, product_id: UUID, user_id: UUID):
    cart = await get_or_create_cart(db, user_id)
    
    stmt = select(CartItem).where(
        CartItem.cart_id == cart.id, 
        CartItem.product_id == product_id
    )
    result = await db.execute(stmt)
    cart_item = result.scalars().first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found")

    if cart_item.quantity <= 1:
        await db.delete(cart_item)
    else:
        cart_item.quantity -= 1
        
    await db.commit()
    return await get_cart_with_items(db, cart.id)

async def clear_cart(db:AsyncSession,user_id:UUID):
    cart = await get_or_create_cart(db, user_id)
    stmt = select(CartItem).where(CartItem.cart_id == cart.id)
    result = await db.execute(stmt)
    cart_items = result.scalars().all()

    for item in cart_items:
        await db.delete(item)

    await db.commit()
    return await get_cart_with_items(db, cart.id)