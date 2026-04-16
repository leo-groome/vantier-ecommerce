"""Helper script to get a JWT token from Neon Auth manually."""

import asyncio
import os
import sys
from getpass import getpass

import httpx
from dotenv import load_dotenv

load_dotenv()


async def get_token() -> None:
    jwks_url = os.getenv("NEON_AUTH_JWKS_URL")
    if not jwks_url:
        print("❌ Missing NEON_AUTH_JWKS_URL in .env")
        sys.exit(1)

    auth_base = jwks_url.replace("/.well-known/jwks.json", "")
    
    print("=== Neon Auth Token Flow ===")
    print("El panel de Neon Auth a veces no deja asignar passwords.")
    print("Vamos a registrarte directo vía API (Sign Up).")
    print("1. Borra tu usuario actual de la consola de Neon (dale al botón rojo Delete User de tu screenshot).")
    print("2. Llena aquí tus datos (el script golpeará /api/auth/sign-up/email).")
    
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    password = getpass("Password nuevo: ")

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{auth_base}/sign-up/email",
                json={"email": email, "password": password, "name": name},
                headers={"Origin": "http://localhost:5173"}
            )
            
            if resp.status_code == 200:
                data = resp.json()
                token = data.get("token")
                new_sub = data.get("user", {}).get("id")
                
                print("\n✅ Sign up exitoso!")
                print(f"Tu nuevo NEON AUTH ID (sub): {new_sub}")
                print("\nTu JWT Token (pégalo en Swagger):")
                print(token)
                
                print("\n--- ¡IMPORTANTE! ---")
                print("1. Usa psql o DataGrip o DBeaver para borrar la fila vieja de tu BD local:")
                print("   DELETE FROM admin_users;")
                print(f"2. Corre: python scripts/seed_owner.py --neon-auth-id {new_sub} --email {email}")
            else:
                print(f"\n❌ Algo falló ({resp.status_code}):")
                print(resp.text)
                
    except Exception as e:
        print(f"\n❌ Error de request: {e}")

if __name__ == "__main__":
    asyncio.run(get_token())
