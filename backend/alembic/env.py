"""Alembic environment configuration for async SQLAlchemy with Neon PostgreSQL."""

import asyncio
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# Load alembic.ini logging config
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Override sqlalchemy.url from environment variable
database_url = os.environ.get("DATABASE_URL", "")
if database_url.startswith("postgresql://"):
    # Ensure asyncpg driver
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql+asyncpg://", 1)
config.set_main_option("sqlalchemy.url", database_url)

# Import all models so Alembic can detect schema changes
# Each slice's models must be imported here for autogenerate to work
from src.core.database import Base, get_engine  # noqa: E402

# Import all model modules to register them with Base.metadata
from src.features.users.models import AdminUser  # noqa: E402, F401
from src.features.products.models import (  # noqa: E402, F401
    Product,
    ProductVariant,
    ProductImage,
)
from src.features.orders.models import Order, OrderItem  # noqa: E402, F401
from src.features.discounts.models import DiscountCode  # noqa: E402, F401
from src.features.exchanges.models import Exchange  # noqa: E402, F401
from src.features.purchase_orders.models import (  # noqa: E402, F401
    PurchaseOrder,
    PurchaseOrderItem,
)
from src.features.inventory.models import OperatingCost, SavedAddress  # noqa: E402, F401

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations without a live database connection (generates SQL script)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Create async engine and run migrations in online mode."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
