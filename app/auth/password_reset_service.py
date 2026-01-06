import secrets
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.password_reset_otp import PasswordResetOTP
from app.auth.services import pwd_context
from sqlalchemy import select



def generate_otp() -> str:
    return str(secrets.randbelow(1000000)).zfill(6)



async def create_password_reset_otp(
    db: AsyncSession,
    email: str
):
    otp = generate_otp()
    otp_hash = pwd_context.hash(otp)

    otp_entry = PasswordResetOTP(
        email=email,
        otp_hash=otp_hash,
        expires_at=datetime.utcnow() + timedelta(minutes=5)
    )

    db.add(otp_entry)
    await db.commit()

    return otp



async def verify_password_reset_otp(
    db: AsyncSession,
    email: str,
    otp: str
) -> bool:
    stmt = (
        select(PasswordResetOTP)
        .where(
            PasswordResetOTP.email == email,
            PasswordResetOTP.is_used == False,
            PasswordResetOTP.expires_at > datetime.utcnow()
        )
        .order_by(PasswordResetOTP.created_at.desc())
    )

    result = await db.execute(stmt)
    otp_entry = result.scalars().first()

    if not otp_entry:
        return False

    if not pwd_context.verify(otp, otp_entry.otp_hash):
        return False

    otp_entry.is_used = True
    await db.commit()
    return True