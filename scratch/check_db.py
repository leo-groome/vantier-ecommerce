import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def check_db():
    db_url = "postgresql+asyncpg://neondb_owner:npg_3FjXAZWBVeL1@ep-still-poetry-ak684mdd-pooler.c-3.us-west-2.aws.neon.tech/neondb?ssl=require"
    engine = create_async_engine(db_url)
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT count(*) FROM products"))
        count = result.scalar()
        print(f"Products count: {count}")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_db())
