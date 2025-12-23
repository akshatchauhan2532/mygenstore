from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.products.schemas import ProductCreate, ProductOut,ProductUpdate
from app.models.product import Product
from app.products.services import add_new_product , get_product_by_id
from app.auth.dependencies import get_current_active_user, require_roles
from uuid import UUID
from sqlalchemy.future import select

router = APIRouter(prefix="/products", tags=["Products"])

@cbv(router)
class ProductRoutes:
    db : AsyncSession = Depends(get_db)  # async session

    @router.get("/product-list",response_model=list[ProductOut])
    async def get_products(self,skip:int=0,limit:int=10):
        result = await self.db.execute(
            select(Product).offset(skip).limit(limit)
        )
        products = result.scalars().all()
        return products

    @router.post("/add",response_model=ProductOut)
    async def add_product(self,product_in:ProductCreate , user = Depends(require_roles(["admin","superadmin"]))):
        product = await add_new_product(self.db,product_in)
        return product
    

    @router.put("/update/{product_id}",response_model=ProductOut)
    async def update_product(self,product_in:ProductUpdate,product_id:UUID ,user = Depends(require_roles(["admin","superadmin"]))):
        product = await get_product_by_id(self.db,product_id)
        if not product:
            raise HTTPException(status_code=404,detail="Product not found")
        
        update_data = product_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(product, field, value)

        await self.db.commit()
        await self.db.refresh(product)

        return product
    
    @router.delete("/delete/{product_id}")
    async def delete_product(self,product_id:UUID,user=Depends(require_roles(["admin","superadmin"]))):
        product = await get_product_by_id(self.db,product_id)
        if not product:
            raise HTTPException(status_code=404,detail="Product not found")
        
        await self.db.delete(product)
        await self.db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)


        