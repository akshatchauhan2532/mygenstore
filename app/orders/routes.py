from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_utils.cbv import cbv
from app.database.session import get_db
from app.orders import services
from app.orders.schemas import PlaceOrderIn, OrderOut, OrderListOut
from app.auth.dependencies import require_roles
from uuid import UUID
from typing import List
router = APIRouter(prefix = "/order", tags=["order"])
@cbv(router)
class orders:
    db : AsyncSession = Depends(get_db)

    @router.post("/place-order",response_model = OrderOut)
    async def make_order(self,order_in:PlaceOrderIn, current_user=Depends(require_roles(["user"]))):
        return await services.place_order(
            db=self.db,
            user_id = current_user.id,
            address_id = order_in.address_id
        )
    
    @router.get("/my-orders",response_model = List[OrderListOut])
    async def fetch_all_orders(self,current_user = Depends(require_roles(["user"]))):
        orders = await services.get_all_orders(self.db,user_id=current_user.id)
        return orders
    
    @router.get("/by-id/{order_id}",response_model=OrderOut)
    async def order_by_id(
        self,
        order_id:UUID,
        current_user = Depends(require_roles(["user"]))
    ):
        order = await services.get_order_by_id(
            db =self.db,
            order_id=order_id,
            user_id=current_user.id
        )
        return order
    

    @router.delete("/{order_id}",response_model=None)
    async def cancel_order(self):
        pass