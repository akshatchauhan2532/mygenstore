
from  app.models.product import Product
from app.products.schemas import ProductCreate, ProductOut
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select

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