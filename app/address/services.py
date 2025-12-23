from uuid import UUID 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.address import UserAddress
from sqlalchemy import update, select,exists

async def create_address(
    db: AsyncSession,
    user_id: UUID,
    address_data: dict
):
    stmt = select(exists().where(
        UserAddress.user_id == user_id,
        UserAddress.is_default == True
    ))
    result = await db.execute(stmt)
    has_default = result.scalar()

    if has_default:
        address_data["is_default"] = False
    else:
        address_data["is_default"] = True

    address = UserAddress(
        user_id=user_id,
        **address_data
    )

    db.add(address)
    await db.commit()
    await db.refresh(address)
    return address
async def update_address(
    db: AsyncSession,
    address_id: UUID,
    user_id: UUID,
    address_data: dict
):
    stmt = (
        update(UserAddress)
        .where(
            UserAddress.id == address_id,
            UserAddress.user_id == user_id
        )
        .values(**address_data)
    )

    result = await db.execute(stmt)
    if result.rowcount == 0:
        return None

    await db.commit()

    stmt = select(UserAddress).where(
        UserAddress.id == address_id,
        UserAddress.user_id == user_id
    )

    result = await db.execute(stmt)
    return result.scalar_one()

async def get_addresses_by_user_id(
        db:AsyncSession,
        user_id:UUID
):
    stmt = select(UserAddress).where(UserAddress.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def delete_address_by_id(
        db:AsyncSession,
        address_id:UUID,
        user_id:UUID
)->bool:
    stmt = select(UserAddress).where(
        UserAddress.id == address_id,
        UserAddress.user_id == user_id
    )
    result = await db.execute(stmt)
    address = result.scalar_one_or_none()

    if not address:
        return False
    
    await db.delete(address)
    await db.commit()
    return True

async def set_default_add(db: AsyncSession, address_id: UUID, user_id: UUID) -> UserAddress:
    stmt = select(UserAddress).where(UserAddress.id == address_id, UserAddress.user_id == user_id)
    result = await db.execute(stmt)
    address = result.scalar_one_or_none()
    
    if not address:
        raise HTTPException(status_code=404, detail="Address not found or not owned by user")
    
    if address.is_default:
        return address
    
    await db.execute(
        update(UserAddress)
        .where(UserAddress.user_id == user_id, UserAddress.is_default == True, UserAddress.id != address_id)
        .values(is_default=False)
    )
    await db.execute(
        update(UserAddress)
        .where(UserAddress.id == address_id, UserAddress.user_id == user_id)
        .values(is_default=True)
    )
    await db.commit()
    
    stmt = select(UserAddress).where(UserAddress.id == address_id, UserAddress.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one()
