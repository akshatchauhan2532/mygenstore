
from  app.models.product import Product
from app.products.schemas import ProductCreate, ProductOut
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional, Dict
from sqlalchemy import select
from sqlalchemy import or_, func

async def add_new_product(db,product_in:ProductCreate):
        product = Product(
            name = product_in.name,
            description = product_in.description,
            price = product_in.price,
            stock = product_in.stock,
        )
        db.add(product)
        await db.commit()
        await db.refresh(product)

        return ProductOut(
            id=str(product.id),
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock,
            is_active=product.is_active
        )


async def get_product_by_id(db,product_id:UUID):
    stmt = select(Product).where(Product.id == product_id)
    result = await db.execute(stmt)
    return result.scalars().first()



async def get_products_paginated(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    search_query: Optional[str] = None,
    filters: Optional[Dict] = None
) -> dict:
    stmt = select(Product).where(Product.is_active == True)
    count_stmt = select(func.count(Product.id)).where(Product.is_active == True)

    if search_query:
        stmt = stmt.where(
            or_(
                Product.name.ilike(f"%{search_query}%"),
                Product.description.ilike(f"%{search_query}%"),
                Product.sku.ilike(f"%{search_query}%")
            )
        )
        count_stmt = count_stmt.where(
            or_(
                Product.name.ilike(f"%{search_query}%"),
                Product.description.ilike(f"%{search_query}%"),
                Product.sku.ilike(f"%{search_query}%")
            )
        )

    if filters:
        if "price_min" in filters:
            stmt = stmt.where(Product.price >= filters["price_min"])
            count_stmt = count_stmt.where(Product.price >= filters["price_min"])
        if "price_max" in filters:
            stmt = stmt.where(Product.price <= filters["price_max"])
            count_stmt = count_stmt.where(Product.price <= filters["price_max"])
        if "in_stock" in filters and filters["in_stock"]:
            stmt = stmt.where(Product.stock > 0)
            count_stmt = count_stmt.where(Product.stock > 0)

    stmt = stmt.offset(skip).limit(limit)

    result = await db.execute(stmt)
    products = result.scalars().all()

    total_result = await db.execute(count_stmt)
    total = total_result.scalar()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "results": [
            ProductOut(
                id=str(p.id),
                name=p.name,
                description=p.description,
                sku=p.sku,
                price=p.price,
                stock=p.stock,
                is_active=p.is_active
            ) for p in products
        ]
    }
