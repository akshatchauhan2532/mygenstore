from __future__ import annotations

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from alembic import context

# Import config
from app.core.config import settings

# Import Base + all models so Alembic can detect changes
from app.database.base import Base

# IMPORT ALL MODELS HERE (IMPORTANT)
from app.models.user import User
from app.models.address import UserAddress
from app.models.product import Product
from app.models.cart_items import CartItem
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.cart import Cart
from app.models.payment import Payment
from app.models.refund import Refund
from app.models.notification import Notification,NotificationMessage

# Alembic Config object
config = context.config

# Logging config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# This tells Alembic what metadata to inspect
target_metadata = Base.metadata


# ---- DB URL FROM Pydantic Settings ----
def get_database_url():
    return settings.DATABASE_URL


# ---- OFFLINE MODE ----
def run_migrations_offline():
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ---- ONLINE MODE (ASYNC) ----
async def run_async_migrations(connection: Connection):
    await connection.run_sync(Base.metadata.create_all)

def do_run_migrations(connection: Connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,      # detects Enum & type changes
        compare_server_default=True
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = create_async_engine(
        get_database_url(),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


# ---- Dispatcher ----
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
