#!/usr/bin/env python3
"""
One-shot Resend connection test.
Reads RESEND_API_KEY directly from .env — no Pydantic Settings, no DB needed.

Usage:
    pyenv exec python scripts/test_resend.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Load .env manually (no pydantic needed)
env_file = Path(__file__).parent.parent / ".env"
for line in env_file.read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        key, _, val = line.partition("=")
        os.environ.setdefault(key.strip(), val.strip())

import httpx  # noqa: E402

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
RESEND_FROM_EMAIL = os.environ.get("RESEND_FROM_EMAIL", "support@vantierluxuryla.com")
RESEND_SUPPORT_EMAIL = os.environ.get("RESEND_SUPPORT_EMAIL", "support@vantierluxuryla.com")


async def main() -> None:
    if not RESEND_API_KEY or RESEND_API_KEY.startswith("re_..."):
        print("❌  RESEND_API_KEY not set in .env — paste your key first.")
        sys.exit(1)

    print(f"🔑  Using key: {RESEND_API_KEY[:8]}***")
    print(f"📤  From: Vantier <{RESEND_FROM_EMAIL}>")
    print(f"📬  To:   {RESEND_SUPPORT_EMAIL}")
    print()

    payload = {
        "from": f"Vantier <{RESEND_FROM_EMAIL}>",
        "to": [RESEND_SUPPORT_EMAIL],
        "subject": "✅ Resend Connection Test — Vantier Backend",
        "text": (
            "This is a connection test from the Vantier backend.\n\n"
            "If you received this email, Resend is correctly configured.\n\n"
            "— Vantier Backend System"
        ),
    }

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
        )

    if resp.status_code in (200, 201):
        data = resp.json()
        print(f"✅  Email sent! ID: {data.get('id')}")
        print(f"    Check inbox: {RESEND_SUPPORT_EMAIL}")
    else:
        print(f"❌  Failed — HTTP {resp.status_code}")
        print(f"    Response: {resp.text}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
