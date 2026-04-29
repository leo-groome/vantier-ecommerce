import asyncio
from src.integrations.envia_client import _ORIGIN_COUNTRY, _ORIGIN_CITY, _ORIGIN_STATE, _ORIGIN_DISTRICT, _PACKAGE, _headers
import json
import httpx
from src.core.config import get_settings

async def main():
    settings = get_settings()
    destination = {
        "country": "US",
        "postalCode": "10001",
        "city": "New York",
        "state": "NY"
    }
    
    payload = {
        "origin": {
            "country": _ORIGIN_COUNTRY,
            "postalCode": "20000",
            "city": _ORIGIN_CITY,
            "state": _ORIGIN_STATE,
        },
        "destination": destination,
        "packages": [_PACKAGE],
        "shipment": {
            "carrier": "dhl", 
            "type": 1
        },
        "customsSettings": {
            "currency": "USD",
            "declaredValue": 50,
            "description": "Clothing",
            "content": "Clothing"
        }
    }
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{settings.envia_base_url}/ship/rate/",
                json=payload,
                headers=_headers(),
            )
            print("Status DHL w/ customsSettings:", resp.status_code)
            print(json.dumps(resp.json(), indent=2)[:500])
            
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())
