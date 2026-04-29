import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv

# Load .env from backend directory relative to this script
dotenv_path = os.path.join(os.path.dirname(__file__), "../backend/.env")
load_dotenv(dotenv_path)

async def check_db():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print(f"Error: DATABASE_URL not found in {dotenv_path}")
        return

    engine = create_async_engine(db_url)
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT count(*) FROM products"))
        count = result.scalar()
        print(f"Products count: {count}")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_db())
