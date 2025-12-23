from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from app.database.session import get_db
from app.address import services  
from sqlalchemy.ext.asyncio import AsyncSession
from app.address.schemas import AddressOut, AddressCreate,AddressUpdate
from app.auth.dependencies import require_roles
from uuid import UUID



router = APIRouter(prefix="/address", tags=["Addresses"])


@cbv(router)
class AddressRoutes:
    db:AsyncSession = Depends(get_db)

    @router.get("/my-addresses",response_model = list[AddressOut])
    async def get_my_addresses(
        self,
        current_user=Depends(require_roles(["user"])),
    ):
        addresses = await services.get_addresses_by_user_id(
            db=self.db,
            user_id=current_user.id
        )
        return addresses

    @router.post("/add",response_model = AddressOut)
    async def add_address(
        self,
        address_in:AddressCreate,
        current_user=Depends(require_roles(["user"])),
    ):
        address = await services.create_address(
            db=self.db,
            user_id=current_user.id,
            address_data=address_in.dict()
        )
        return address
    
    @router.put("/update/{address_id}",response_model= AddressOut)
    async def update_address(
        self,
        address_id:UUID,
        address_in:AddressUpdate,
        current_user=Depends(require_roles(["user"])),
    ):
        updated_address = await services.update_address(
            db = self.db,
            address_id=address_id,
            user_id=current_user.id,
            address_data=address_in.dict(exclude_unset=True)
        )
        if not updated_address:
            raise HTTPException(
                status_code=404,
                detail="Address not found or not owned by user"
            )
        return updated_address
    
    @router.delete("/delete/{address_id}",response_model = None)
    async def delete_address(
        self,
        address_id:UUID,
        current_user = Depends(require_roles(["user"]))
    ):
        is_deleted = await services.delete_address_by_id(
            db = self.db,
            address_id=address_id,
            user_id = current_user.id
        )
        if not is_deleted:
            raise HTTPException(status_code =404,detail="Address not found")
        return None
    
    @router.put("/set-default/{address_id}",response_model=AddressOut)
    async def set_default_address(
        self,
        address_id:UUID,
        current_user = Depends(require_roles(["user"]))

    ):
        address = await services.set_default_add(
            db = self.db ,
            address_id=address_id,
            user_id = current_user.id
        )
        if not address:
            raise HTTPException(status_code=404,detail="Address not found or not owned by user")
        
        return address
