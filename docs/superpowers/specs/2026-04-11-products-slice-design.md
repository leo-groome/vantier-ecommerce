# Products Slice — Design Spec

**Date:** 2026-04-11
**Status:** Approved
**Scope:** Full CRUD admin + public catalog for `src/features/products/`

---

## Context

First feature slice to implement in Vantier e-commerce backend. Products are the foundation — orders, inventory, and exchanges all depend on `product_variants`. The slice must expose a public catalog for the storefront and full admin CRUD for the owner panel.

---

## Approach

Single `APIRouter` with per-endpoint auth guards (not split routers). Keeps VSA slice cohesive in one file, explicit guards per endpoint, easy to extend.

---

## Endpoints

```
# Public (no auth)
GET  /api/v1/products                                   → paginated list of active products
GET  /api/v1/products/{product_id}                      → product detail with variants + images

# Admin read (AdminUserDep)
GET  /api/v1/products?include_inactive=true             → includes inactive products/variants

# Owner write — products (OwnerDep)
POST   /api/v1/products                                 → create product
PATCH  /api/v1/products/{product_id}                    → partial update
DELETE /api/v1/products/{product_id}                    → soft-delete (is_active=False)

# Owner write — variants (OwnerDep)
POST   /api/v1/products/{product_id}/variants           → add variant (SKU auto-generated)
PATCH  /api/v1/products/{product_id}/variants/{vid}     → partial update
DELETE /api/v1/products/{product_id}/variants/{vid}     → soft-delete

# Admin write — images (AdminUserDep, receives pre-uploaded URLs)
POST   /api/v1/products/{product_id}/variants/{vid}/images
DELETE /api/v1/products/{product_id}/variants/{vid}/images/{iid}   → hard delete
PATCH  /api/v1/products/{product_id}/variants/{vid}/images/reorder → update positions
```

---

## Schemas (`src/features/products/schemas.py`)

### Input
| Schema | Fields |
|--------|--------|
| `ProductCreate` | `line` (enum), `name`, `description?` |
| `ProductUpdate` | `name?`, `description?`, `is_active?` |
| `VariantCreate` | `style`, `size`, `color`, `cost_acquisition_usd`, `price_usd`, `stock_qty=0` |
| `VariantUpdate` | all fields optional |
| `ImageCreate` | `url`, `alt_text?`, `position=0` |
| `ImageReorder` | `image_ids: list[UUID]` |

### Output
| Schema | Notes |
|--------|-------|
| `ImageResponse` | `id, url, position, alt_text` |
| `VariantResponse` | includes `images`; `cost_acquisition_usd` excluded from public schema |
| `VariantAdminResponse` | extends VariantResponse, adds `cost_acquisition_usd` |
| `ProductResponse` | includes `variants: list[VariantResponse]` |
| `ProductListResponse` | `items, total, page, page_size` |

---

## Service (`src/features/products/service.py`)

| Function | Description |
|----------|-------------|
| `list_products(db, filters, pagination, include_inactive)` | SELECT + JOINs, filters: line/style/size/in_stock |
| `get_product(db, product_id)` | eager-load variants→images; raises `NotFoundException` |
| `create_product(db, data)` | INSERT |
| `update_product(db, product_id, data)` | partial PATCH; raises `NotFoundException` |
| `deactivate_product(db, product_id)` | SET is_active=False |
| `add_variant(db, product_id, data)` | generates SKU via `utils.generate_sku()`; generates barcode |
| `update_variant(db, variant_id, data)` | partial PATCH |
| `deactivate_variant(db, variant_id)` | SET is_active=False |
| `add_image(db, variant_id, data)` | INSERT |
| `remove_image(db, image_id)` | DELETE (hard) |
| `reorder_images(db, variant_id, image_ids)` | bulk UPDATE position |

---

## Business Rules

- **SKU always auto-generated** — never accepted from client input
- **Soft-delete** on Product and ProductVariant — preserves FK integrity with `orders` table
- **Hard-delete** only on ProductImage — no FK references from orders
- **`cost_acquisition_usd`** never exposed in public-facing responses
- **`include_inactive`** query param only has effect when caller is `AdminUserDep`; public callers always get active-only regardless

---

## Files Modified

| File | Action |
|------|--------|
| `src/features/products/schemas.py` | Create |
| `src/features/products/service.py` | Create |
| `src/features/products/router.py` | Create |
| `src/main.py` | Uncomment products router import + `app.include_router(...)` |

---

## Dependencies Reused

- `src/core/utils.py` → `generate_sku()`, `generate_barcode_value()`, `paginate()`
- `src/core/dependencies.py` → `AdminUserDep`, `OwnerDep`, `DBSession`
- `src/core/exceptions.py` → `NotFoundException`
- `src/features/products/models.py` → `Product`, `ProductVariant`, `ProductImage`

---

## Verification

```bash
# Start server
cd backend && uvicorn src.main:app --reload

# Smoke tests
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/products

# With auth (owner token)
curl -X POST http://localhost:8000/api/v1/products \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"line":"polo_atelier","name":"Test Product"}'
```
