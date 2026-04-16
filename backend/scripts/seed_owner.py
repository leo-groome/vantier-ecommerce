"""Seed the first owner user manually.

Run this script to inject the first owner row into the database,
using your Neon Auth `sub` (user ID) from a valid JWT.

Usage:
    python scripts/seed_owner.py --neon-auth-id <sub_id> --email <email>
"""

import argparse
import asyncio
import sys
from uuid import uuid4

from sqlalchemy import func, select

from src.core.database import get_session_factory
from src.features.users.models import AdminUser


async def run_seed(neon_id: str, email: str) -> None:
    """Seed the first admin into the database."""
    async with get_session_factory()() as db:
        # Prevent seeding if any user exists
        count_res = await db.execute(select(func.count(AdminUser.id)))
        count = count_res.scalar_one()

        if count > 0:
            print(f"❌ Error: Database already has {count} admin users.")
            print("To add more, use the /api/v1/users/invite endpoint as an owner.")
            sys.exit(1)

        print(f"Seeding owner: {email} ({neon_id})...")

        obj = AdminUser(
            id=uuid4(),
            neon_auth_user_id=neon_id,
            email=email,
            role="owner",
            is_active=True
        )
        db.add(obj)
        await db.commit()

        print("✅ Success! You can now log into the API as an owner.")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Seed first owner in Vantier")
    parser.add_argument("--neon-auth-id", required=True, help="Neon Auth 'sub' claim")
    parser.add_argument("--email", required=True, help="Email address of the owner")

    args = parser.parse_args()

    asyncio.run(run_seed(args.neon_auth_id, args.email))


if __name__ == "__main__":
    main()
