"""Integration tests for products API endpoints."""

import uuid
from decimal import Decimal

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.products.models import Product, ProductImage, ProductVariant


@pytest.mark.asyncio
async def test_list_products_public(client: AsyncClient, db_session: AsyncSession):
    """Public endpoint returns active products."""
    product = Product(line="polo_atelier", name="Public Polo")
    db_session.add(product)
    await db_session.flush()

    resp = await client.get("/api/v1/products")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "total" in data
    names = [p["name"] for p in data["items"]]
    assert "Public Polo" in names


@pytest.mark.asyncio
async def test_get_product_public(client: AsyncClient, db_session: AsyncSession):
    """Public endpoint returns a single product by ID."""
    product = Product(line="signature", name="Detail Test")
    db_session.add(product)
    await db_session.flush()

    resp = await client.get(f"/api/v1/products/{product.id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Detail Test"


@pytest.mark.asyncio
async def test_get_product_not_found(client: AsyncClient):
    resp = await client.get(f"/api/v1/products/{uuid.uuid4()}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_create_product_requires_owner(client: AsyncClient):
    resp = await client.post("/api/v1/products", json={"line": "essential", "name": "X"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_create_product_as_owner(owner_client: AsyncClient, db_session: AsyncSession):
    resp = await owner_client.post(
        "/api/v1/products",
        json={"line": "polo_atelier", "name": "New Owner Product"}
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "New Owner Product"
    assert data["line"] == "polo_atelier"
    assert data["variants"] == []


@pytest.mark.asyncio
async def test_update_product_as_owner(owner_client: AsyncClient, db_session: AsyncSession):
    product = Product(line="essential", name="Before Update")
    db_session.add(product)
    await db_session.flush()

    resp = await owner_client.patch(
        f"/api/v1/products/{product.id}",
        json={"name": "After Update"}
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "After Update"


@pytest.mark.asyncio
async def test_deactivate_product_as_owner(owner_client: AsyncClient, db_session: AsyncSession):
    product = Product(line="signature", name="To Delete")
    db_session.add(product)
    await db_session.flush()

    resp = await owner_client.delete(f"/api/v1/products/{product.id}")
    assert resp.status_code == 204


@pytest.mark.asyncio
async def test_add_variant_as_owner(owner_client: AsyncClient, db_session: AsyncSession):
    product = Product(line="polo_atelier", name="Variant Parent")
    db_session.add(product)
    await db_session.flush()

    resp = await owner_client.post(
        f"/api/v1/products/{product.id}/variants",
        json={
            "style": "classic",
            "size": "M",
            "color": "Black",
            "cost_acquisition_usd": "50.00",
            "price_usd": "120.00",
        }
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["sku"].startswith("VAT-PA-CL-M-BLACK-")
    assert "cost_acquisition_usd" not in data  # not exposed publicly


@pytest.mark.asyncio
async def test_add_image_as_admin(admin_client: AsyncClient, db_session: AsyncSession):
    product = Product(line="essential", name="Image Parent")
    db_session.add(product)
    await db_session.flush()

    sku = f"VAT-ES-CL-M-RED-{uuid.uuid4().hex[:4].upper()}"
    variant = ProductVariant(
        product_id=product.id, style="classic", size="M", color="Red",
        sku=sku, barcode=sku, stock_qty=5,
        cost_acquisition_usd=Decimal("30.00"), price_usd=Decimal("80.00"),
    )
    db_session.add(variant)
    await db_session.flush()

    resp = await admin_client.post(
        f"/api/v1/products/{product.id}/variants/{variant.id}/images",
        json={"url": "https://cdn.test/photo.jpg", "position": 0}
    )
    assert resp.status_code == 201
    assert resp.json()["url"] == "https://cdn.test/photo.jpg"
