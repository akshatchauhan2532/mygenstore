from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_utils.cbv import cbv
from app.database.session import get_db
from app.cart import services
from app.cart.schemas import AddToCartIn, CartOut
from app.auth.dependencies import require_roles
from uuid import UUID

router = APIRouter(prefix="/cart", tags=["Cart"])


@cbv(router)
class CartRoutes:
    db: AsyncSession = Depends(get_db)  # async session


    @router.get("/my-cart", response_model=CartOut)
    async def get_my_cart(
        self,
        current_user=Depends(require_roles(["user"])),
    ):
        cart = await services.get_cart_by_user_id(self.db, user_id=current_user.id)
        return cart

    @router.post("/add-item", response_model=CartOut)
    async def add_item(
        self,
        item_in: AddToCartIn,
        current_user=Depends(require_roles(["user"])),
    ):
        cart_item = await services.add_item_to_cart(
            self.db,
            user_id=current_user.id,
            product_id=item_in.product_id,
            quantity=item_in.quantity,
        )
        return cart_item
    

    @router.delete("/delete/{product_id}",response_model=CartOut)
    async def  delete_item(
        self,
        product_id:UUID,
        current_user=Depends(require_roles(["user"])),
    ):
        cart = await services.delete_item_from_cart(
            self.db,
            user_id=current_user.id,
            product_id=product_id,
        )
        return cart
    

    @router.patch("/increment/{product_id}",response_model=CartOut)
    async def increment_item(
        self,
        product_id:UUID,
        current_user=Depends(require_roles(["user"])),
    ):
        return await services.increment_by_one(
            self.db,
            product_id=product_id,
            user_id=current_user.id,
        )
    
    @router.patch("/decrement/{product_id}",response_model=CartOut)
    async def decrement_item(
        self,
        product_id:UUID,
        current_user=Depends(require_roles(["user"])),
    ):
        return await services.decrement_by_one(
            self.db,
            product_id=product_id,
            user_id=current_user.id,
        )

    @router.delete("/clear",response_model=CartOut)
    async def clear_cart(
        self,
        current_user=Depends(require_roles(["user"])),
    ):
        return await services.clear_cart(
            self.db,
            user_id=current_user.id,
        )