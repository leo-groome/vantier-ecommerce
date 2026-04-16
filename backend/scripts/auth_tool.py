"""Vantier Auth CLI — get a real JWT from Neon Auth in one command.

Usage:
    python scripts/auth_tool.py signin  --email EMAIL
    python scripts/auth_tool.py signup  --email EMAIL --name NAME

The token is printed and (if xclip/xsel/pbcopy is available) copied to clipboard.
Use it in Swagger: Authorization → Bearer <token>
Use it in pytest:  os.environ["TEST_JWT"] or pipe stdout.

Neon Auth endpoint is read from NEON_AUTH_JWKS_URL in .env.
"""

import argparse
import asyncio
import os
import subprocess
import sys
from getpass import getpass

import httpx
from dotenv import load_dotenv

load_dotenv()


def _get_auth_base() -> str:
    jwks_url = os.getenv("NEON_AUTH_JWKS_URL", "")
    if not jwks_url:
        print("❌ NEON_AUTH_JWKS_URL not set in .env", file=sys.stderr)
        sys.exit(1)
    # Strip JWKS path → base auth URL
    # e.g. https://ep-xyz.neonauth.../neondb/auth/.well-known/jwks.json
    #    → https://ep-xyz.neonauth.../neondb/auth
    base = jwks_url.replace("/.well-known/jwks.json", "")
    return base


def _copy_to_clipboard(text: str) -> bool:
    """Try to copy to clipboard. Returns True on success."""
    for cmd in (["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"], ["pbcopy"]):
        try:
            proc = subprocess.run(cmd, input=text.encode(), check=True, capture_output=True)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
    return False


async def _get_jwt_from_session(client: httpx.AsyncClient, base: str, session_token: str) -> str | None:
    """Exchange an opaque session token for a JWT using Neon Auth's /token endpoint.
    
    Better Auth JWT plugin: GET /token with opaque session token as Bearer.
    """
    # Try Authorization header first (Better Auth JWT plugin standard)
    for attempt in [
        # Method 1: Authorization Bearer header
        lambda: client.get(
            f"{base}/token",
            headers={"Authorization": f"Bearer {session_token}", "Origin": "http://localhost:5173"},
        ),
        # Method 2: Cookie-based (fallback)
        lambda: client.get(
            f"{base}/token",
            cookies={"better-auth.session_token": session_token},
            headers={"Origin": "http://localhost:5173"},
        ),
    ]:
        try:
            resp = await attempt()
            if resp.status_code == 200:
                data = resp.json()
                jwt_token = data.get("token") or data.get("jwt") or data.get("access_token")
                if jwt_token and jwt_token.startswith("eyJ"):
                    return jwt_token
        except Exception:
            continue
    return None


async def do_signin(email: str, password: str) -> None:
    base = _get_auth_base()
    print(f"\n🔐 Signing in as {email}...")

    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.post(
            f"{base}/sign-in/email",
            json={"email": email, "password": password},
            headers={
                "Content-Type": "application/json",
                "Origin": "http://localhost:5173",
            },
            timeout=15,
        )

    if resp.status_code not in (200, 201):
        print(f"❌ Sign-in failed ({resp.status_code}):\n{resp.text}", file=sys.stderr)
        sys.exit(1)

    data = resp.json()

    # The 'token' in the sign-in response is an OPAQUE session token, not a JWT.
    # We must exchange it for a real JWT via GET /token.
    opaque_token = data.get("token")
    token = None

    if opaque_token:
        async with httpx.AsyncClient() as client:
            token = await _get_jwt_from_session(client, base, opaque_token)

    # Last resort: maybe this IS already a JWT (future Neon Auth versions)
    if not token and opaque_token and opaque_token.startswith("eyJ"):
        token = opaque_token

    if not token:
        print("⚠️  Could not obtain a JWT from Neon Auth.")
        print(f"   Opaque session token received: {opaque_token}")
        print("\n   This means the JWT plugin response format may differ.")
        print("   Check: does your Neon Auth instance have the JWT plugin enabled?")
        print("   Raw sign-in response:")
        print(f"   {data}")
        sys.exit(1)

    _print_token(token, data)



async def do_signup(email: str, password: str, name: str) -> None:
    base = _get_auth_base()
    print(f"\n📝 Signing up {name} <{email}>...")

    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.post(
            f"{base}/sign-up/email",
            json={"email": email, "password": password, "name": name},
            headers={
                "Content-Type": "application/json",
                "Origin": "http://localhost:5173",
            },
            timeout=15,
        )

    if resp.status_code not in (200, 201):
        print(f"❌ Sign-up failed ({resp.status_code}):\n{resp.text}", file=sys.stderr)
        sys.exit(1)

    data = resp.json()
    token = data.get("token") or data.get("jwt") or data.get("access_token")

    if not token:
        session_cookie = resp.cookies.get("better-auth.session_token")
        if session_cookie:
            async with httpx.AsyncClient() as client:
                token = await _get_jwt_from_session(client, base, session_cookie)

    if not token:
        user_id = data.get("user", {}).get("id", "UNKNOWN")
        print(f"\n✅ Sign-up OK. Neon Auth ID (sub): {user_id}")
        print("⚠️  No JWT returned. Seed the owner manually:")
        print(f"   python scripts/seed_owner.py --neon-auth-id {user_id} --email {email}")
        sys.exit(0)

    _print_token(token, data)


def _print_token(token: str, data: dict) -> None:
    user = data.get("user", {})
    neon_id = user.get("id") or data.get("sub", "?")
    email = user.get("email") or data.get("email", "?")

    print(f"\n✅ Authenticated! Neon Auth ID: {neon_id}")
    print(f"   Email: {email}")
    print("\n" + "=" * 60)
    print("JWT TOKEN (Bearer):")
    print("=" * 60)
    print(token)
    print("=" * 60)

    copied = _copy_to_clipboard(token)
    if copied:
        print("\n📋 Token copied to clipboard. Paste in Swagger: Authorization → Bearer <token>")
    else:
        print("\n💡 No clipboard util found (install xclip). Copy the token above manually.")

    print(f"\n📌 To seed DB as owner:")
    print(f"   python scripts/seed_owner.py --neon-auth-id {neon_id} --email {email}")


def main():
    parser = argparse.ArgumentParser(
        description="Vantier Auth CLI — get a real JWT from Neon Auth",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # signin
    p_signin = sub.add_parser("signin", help="Sign in to existing account")
    p_signin.add_argument("--email", required=True)
    p_signin.add_argument("--password", help="If omitted, prompted securely")

    # signup
    p_signup = sub.add_parser("signup", help="Create new account (first-time setup)")
    p_signup.add_argument("--email", required=True)
    p_signup.add_argument("--name", required=True)
    p_signup.add_argument("--password", help="If omitted, prompted securely")

    args = parser.parse_args()

    password = args.password or getpass(f"Password for {args.email}: ")

    if args.command == "signin":
        asyncio.run(do_signin(args.email, password))
    elif args.command == "signup":
        asyncio.run(do_signup(args.email, password, args.name))


if __name__ == "__main__":
    main()
