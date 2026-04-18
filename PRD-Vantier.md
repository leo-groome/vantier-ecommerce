# PRD — Vantier E-Commerce Platform

---

## 1. Executive Summary

Vantier is a premium men's clothing brand based in Mexico, targeting the Los Angeles (U.S.) market with international shipping capabilities. The objective is to build a full-stack, production-ready e-commerce platform that allows Vantier to sell its three product lines nationally and internationally, automate logistics and financial reporting, and deliver a luxury digital experience consistent with its brand identity.

---

## 2. Business Context

| Item | Detail |
|---|---|
| Brand | Vantier |
| Primary Market | Los Angeles, CA (USA) + International |
| Warehouse | Single warehouse in Mexico |
| Currency | USD ($) |
| Language | English (primary) |
| Support Email | luxury@vantiersupport.com |
| Min Profit Margin | 50% per garment (enforced by system) |
| Prices include IVA | Yes — shipping cost added at checkout |
| Free Shipping Threshold | 5+ items (any category combination) |
| Package Standard | 33 × 26 × 10 cm |

---

## 3. Product Catalog

### 3.1 Lines & Sizes

| Line | Type | Sizes | Classic Price | Design Price |
|---|---|---|---|---|
| Polo Atelier | Jacket | S, M, L, XL, XXL | TBD (USD) | TBD (USD) |
| Signature | Shirt | S, M, L, XL, XXL, XXXL | TBD (USD) | TBD (USD) |
| Essential | T-Shirt | S, M, L | TBD (USD) | TBD (USD) |

> **Note:** Client must confirm USD pricing before development of the checkout module (Phase 2).

### 3.2 Product Variants
Each SKU is defined by: **Line × Style (Classic/Design) × Size × Color**
The system auto-generates unique barcodes/SKUs for each variant, printable from the admin panel.

SKU format: `VAT-{LINE}-{STYLE}-{SIZE}-{COLOR}-{SUFFIX}` (e.g. `VAT-PA-CL-M-BLACK-A3F2`)

### 3.3 Inventory Rules
- Total current stock: ~80 garments
- Low stock alert triggers at: **50 total units**
- Supplier lead time: **4–7 business days** (purchase order module required)

---

## 4. Goals & Success Metrics

| Goal | Metric |
|---|---|
| Enable direct-to-consumer sales online | First order processed within 2 weeks of launch |
| Automate logistics | 100% of shipping labels generated via envia.com API |
| Financial visibility | Real-time net profit dashboard in admin panel |
| Margin protection | System blocks/alerts on discounts that break 50% margin floor |
| Customer trust | Transactional email coverage: 100% of order events |

---

## 5. User Personas

### 5.1 Customer (Storefront)
- **Profile:** Men aged 25–40, fashion-conscious, based in LA or international markets
- **Needs:** Browse by product line, select size/color, checkout securely, track order
- **Auth:** Neon Auth (email/social login)

### 5.2 Admin — Owner
- **Access:** Full platform access (inventory, orders, financials, settings, users)
- **Needs:** Profitability dashboards, stock management, discount codes, shipping labels

### 5.3 Admin — Operative
- **Access:** Inventory + Orders only (no financials, no settings)
- **Needs:** Process orders, update stock, generate shipping labels, log exchanges

---

## 6. Functional Requirements

### 6.1 Storefront (Customer-Facing)

#### Homepage
- Hero section with brand imagery and CTA
- Product line grid (Polo Atelier, Signature, Essential)
- Featured products / new arrivals section
- Brand statement / value proposition block

#### Product Catalog
- Filter by: line, size, style (Classic / Design), color
- Product card with: image, name, price (USD), available sizes
- "Low stock" badge when variant stock < threshold

#### Product Detail Page (PDP)
- Image gallery (multiple photos per variant)
- Size selector (only in-stock sizes shown as active)
- Color/style selector
- "Add to cart" button
- Size guide modal
- Shipping estimate widget (based on destination ZIP)
- Exchange policy note (no returns, same-category exchange only)

#### Shopping Cart
- Real-time subtotal
- Free shipping banner: "Add X more item(s) for free shipping"
- Automatic free shipping applied at 5+ items
- Promo/discount code field
- Proceed to checkout CTA

#### Checkout (Stripe)
- Guest checkout + authenticated checkout
- Shipping address (international support)
- Shipping cost calculated in real-time via envia.com API
- Order summary with line items, shipping, total in USD
- Stripe payment form (card, Apple Pay, Google Pay via Stripe)
- Order confirmation screen + email trigger

#### User Account
- Order history with status tracking
- Exchange request form per order (routes to luxury@vantiersupport.com via Resend)
- Saved shipping addresses

#### Contact
- Contact form (sends to luxury@vantiersupport.com via Resend)
- Policy pages: Exchange policy, Shipping policy

---

### 6.2 Admin Panel

#### Dashboard (Owner only)
- Real-time metrics: Total revenue, COGS, net profit, margin %
- Today / 7-day / 30-day / custom range filters
- Top-selling SKUs
- Pending orders count
- Low stock alert banner
- [x] Profit margin alert: visual warning in Frontend when any product's effective margin < 50%

#### Inventory Management
- CRUD for products, variants (size, color, style)
- Stock adjustment per variant
- Barcode / SKU auto-generation (printable PDF labels)
- Bulk import/export (CSV)
- Cost of acquisition field per variant (used for margin calculation)
- Operating cost field (packaging + labels + commission baseline: ~$580 MXN equivalent)

#### Purchase Orders Module
- Create PO to supplier with expected items and quantities
- Track PO status: Ordered → In Transit → Received
- Auto-increment stock on receive confirmation
- Expected arrival date field (used for "back in stock" logic)

#### Order Management
- Order list with filters: status, date, customer
- Order detail view: items, shipping address, total, payment status
- Update order status: Pending → Processing → Shipped → Delivered
- Generate shipping label via envia.com API (auto-fills package dimensions 33×26×10cm)
- Mark exchange requests: log which variant was sent as replacement

#### Financial Dashboard (Owner only)
- Per-product profitability: sale price − COGS − operating costs = net profit
- Profitability alert configuration (min 50% margin floor)
- Break-even simulation tool
- Revenue/expense export (CSV)

#### Discount Codes
- Create/edit/disable coupon codes
- Types: % off (max 100%), fixed amount off
- System validation: visual warning when discount reduces margin below 50% floor
- Usage limit and expiration date per code

#### User Management
- Two roles: Owner, Operative
- Invite team members by email (Neon Auth)
- Role-based access control enforced in API middleware

---

### 6.3 Email Notifications (Resend)

| Trigger | Recipient | Content |
|---|---|---|
| Order placed | Customer | Order confirmation, items, total, estimated shipping |
| Order shipped | Customer | Tracking number, carrier link |
| Exchange requested | Admin + Customer | Exchange details, return instructions |
| Low stock alert | Admin (Owner) | SKU + current stock level |
| New order | Admin (Operative) | Order summary notification |
| Contact form submitted | Admin | Customer message + contact info |

---

## 7. Non-Functional Requirements

| Requirement | Target |
|---|---|
| Performance | LCP < 2.5s on product pages |
| Availability | 99.9% uptime (Neon.tech + serverless) |
| Security | All endpoints authenticated; RBAC enforced server-side; Stripe webhook signature verification |
| SEO | SSR/SSG for storefront pages (Vue with proper meta tags, OG tags) |
| Mobile | Fully responsive; mobile-first design |
| Accessibility | WCAG 2.1 AA compliant |
| Scalability | Stateless FastAPI; Neon autoscales; no horizontal scaling blockers |

---

## 8. Tech Stack

### Backend
| Layer | Technology |
|---|---|
| API Framework | **FastAPI** (Python 3.12+) |
| Database | **Neon.tech** (PostgreSQL, serverless) |
| ORM | **SQLAlchemy 2.0** + Alembic migrations |
| Authentication | **Neon Auth** (JWT verification via JWKS — replaces Clerk) |
| Email | **Resend** (transactional via REST API) |
| Payments | **Stripe** (Checkout Sessions + Webhooks) |
| Shipping | **envia.com API** (rate calculation + label generation) |
| Barcode Gen | `python-barcode` + `qrcode` |
| PDF Labels | `reportlab` |

### Frontend
| Layer | Technology |
|---|---|
| Framework | **Vue.js 3** (Composition API) |
| Styling | **Tailwind CSS v3** |
| State | **Pinia** |
| Routing | **Vue Router 4** |
| Auth UI | **Neon Auth SDK** |
| HTTP Client | **Axios** or `ofetch` |
| Forms | **VeeValidate + Zod** |
| Payments UI | **Stripe.js + Vue Stripe** |

### Infrastructure
| Layer | Technology |
|---|---|
| DB | Neon.tech (PostgreSQL) |
| Backend Deploy | Railway / Render (FastAPI container) |
| Frontend Deploy | Vercel (Vue SPA or SSR via Nitro) |
| File Storage | Cloudflare R2 or Supabase Storage (product images) |
| Environment | `.env` managed per environment |

---

## 9. Data Model

All 12 tables are implemented in `backend/src/features/*/models.py` and managed via Alembic migrations.

```
admin_users       (id, neon_auth_user_id, email, role: owner|operative, is_active)

products          (id, line: polo_atelier|signature|essential, name, description, is_active)

product_variants  (id, product_id, style: classic|design, size, color, sku, barcode,
                   stock_qty, cost_acquisition_usd, price_usd, is_active)

product_images    (id, variant_id, url, position, alt_text)

saved_addresses   (id, neon_auth_user_id, label, full_name, line1, line2, city, state,
                   zip, country, phone, is_default)

orders            (id, neon_auth_user_id [nullable=guest], customer_email, status,
                   payment_status, subtotal_usd, shipping_usd, discount_usd, total_usd,
                   shipping_address [JSONB], is_free_shipping, stripe_payment_intent_id,
                   carrier_tracking_number, envia_shipment_id, envia_label_url,
                   discount_code_id)

order_items       (id, order_id, variant_id, qty, unit_price_usd)

discount_codes    (id, code, type: percent|fixed, value [percent max 100],
                   usage_limit, usage_count, expires_at, is_active)

exchanges         (id, order_id, original_variant_id, replacement_variant_id [nullable],
                   status: requested|approved|shipped|completed|rejected,
                   customer_notes, admin_notes)

purchase_orders   (id, reference_number, supplier_name, expected_arrival_date,
                   status: ordered|in_transit|received, created_by_user_id)

purchase_order_items (id, po_id, variant_id, qty_ordered, qty_received)

operating_costs   (id, label, amount_usd, is_recurring, notes)
```

**Key DB constraints:**
- `product_variants.price_usd > 0`, `stock_qty >= 0`, `cost_acquisition_usd >= 0`
- `order_items.qty > 0`
- `discount_codes.value > 0`, percent discounts `value <= 100`
- `purchase_order_items.qty_ordered > 0`, `qty_received >= 0`
- One default saved address per user (partial unique index)

---

## 10. Business Logic & Policies

### Shipping
- Real-time rate from envia.com API using fixed dimensions 33×26×10 cm
- Free shipping automatically applied when total `qty >= 5` across all order items
- International shipping supported (envia.com covers cross-border from Mexico)

### Pricing & Margins
- All prices stored and displayed in USD (`decimal.Decimal`, not float)
- Margin formula: `(sale_price − cost_acquisition − sum(operating_costs)) / sale_price ≥ 0.50`
- Discount codes validated server-side; rejected if margin floor breached
- Financial dashboard shows: revenue, COGS, operating costs, net profit, margin %

### Exchanges (no returns)
- Customer initiates via account portal or contact form
- Same product line/category only (enforced in service layer)
- Admin logs exchange in system; shipping cost covered by Vantier
- Resend triggers notification emails to both parties

### Barcodes / SKUs
- Auto-generated on variant creation: format `VAT-{LINE}-{STYLE}-{SIZE}-{COLOR}-{SUFFIX}`
- Suffix is a 4-character hex token (UUID-based) — collision-safe, no race conditions
- Printable as PDF barcode label from admin panel

### Authentication
- All JWT tokens issued and verified via **Neon Auth** (JWKS endpoint, Ed25519/OKP keys)
- Admin roles (`owner`, `operative`) stored in `admin_users` table, keyed by Neon Auth user ID
- Storefront customers authenticated via Neon Auth; their user IDs stored as strings on orders/addresses (no FK)
- Guest checkout supported (`neon_auth_user_id` nullable on orders)

#### Auth Architecture Notes (Recorded 2026-04-14, updated 2026-04-17)

**Flow de producción correcto:**
1. Frontend Vue usa `@neondatabase/auth` SDK (wraps Better Auth) para sign-in/sign-up.
2. SDK emite una *cookie de sesión opaca* internamente (Better Auth).
3. El servidor Neon Auth inyecta el JWT real en el header `set-auth-jwt` de cada response exitoso.
4. El SDK intercepta este header y reemplaza `session.token` con el JWT (`eyJ...`, EdDSA/Ed25519).
5. El interceptor Axios llama `authClient.getSession()` → extrae `data.session.token` → envía como `Authorization: Bearer <jwt>`.
6. FastAPI valida el JWT contra JWKS. Cero contraseñas en el backend.

**Configuración crítica de NEON_AUTH_AUDIENCE:**
- El JWT emitido por Neon Auth tiene `aud = <Neon Auth URL>` (e.g. `https://ep-still-poetry-ak684mdd.neonauth.c-3.us-west-2.aws.neon.tech`).
- **No** es `"authenticated"` — ese valor es de Supabase. Configuring `NEON_AUTH_AUDIENCE=authenticated` causa 401 en todos los endpoints.
- El valor correcto en `backend/.env`: `NEON_AUTH_AUDIENCE=<URL base de NEON_AUTH_JWKS_URL sin el path>`.
- Bug corregido 2026-04-17: actualizado en `backend/.env`.

**Por qué el script CLI no emite JWT directamente:**
- Neon Auth usa Better Auth internamente. El endpoint `/sign-in/email` retorna un *token de sesión opaco* (no un JWT).
- El intercambio sesión → JWT requiere una cookie de browser activa con binding de sesión completo. No funciona desde CLI/Postman por diseño de seguridad de Better Auth.
- Esto es correcto y esperado. El JWT se obtiene solo a través del SDK del browser.

**Dev bypass (local únicamente):**
- `ENABLE_DEV_AUTH=true` en `.env` activa tokens `dev_token_<neon_id>` para QA sin red.
- **NUNCA se debe poner en `.env` de producción o staging.**
- El bypass está bloqueado a nivel de código si `ENVIRONMENT=production`.
- Para Swagger local: `dev_token_e552ac1b-527c-4237-a6b0-08821d854a59` (owner seeded).
- ⚠️ El dev bypass requiere que el proceso haya arrancado con `ENABLE_DEV_AUTH=true` — si Uvicorn arrancó antes de agregarlo al `.env`, reiniciar el servidor.

**Auth policy (2026-04-17):**
- Auth es **exclusivo para admins** (`owner`, `operative`). Los clientes compran sin registrarse (guest checkout).
- Las rutas de storefront (`/account`, `/orders`, `/exchanges`) son públicas — sin `requireAuth`.
- La ruta `/auth/login` tiene `guestOnly: true` — si el admin ya está autenticado, redirige automáticamente a `/admin/dashboard`.
- El guard `requireAdmin` en `/admin/*` verifica el role desde localStorage (`Owner` | `Operative`).
- Login → JWT verificado → `/users/me` retorna role → `fetchRole()` guarda en localStorage → redirect a `/admin/dashboard`. ✅ Flujo completo verificado 2026-04-17.

---

## 11. Development Roadmap

### Phase 1 — Foundation ✅ COMPLETE

**Backend infrastructure (100% done):**
- [x] Project scaffolding: FastAPI + Neon PostgreSQL + pyenv virtualenv (`vantier-backend`, Python 3.12.7)
- [x] Neon Auth JWT middleware (`src/core/auth.py`) — JWKS-based RS256 verification
- [x] Async SQLAlchemy 2.0 engine + session factory (`src/core/database.py`)
- [x] Pydantic v2 settings from `.env` (`src/core/config.py`)
- [x] RBAC dependencies: `get_current_user`, `get_admin_user`, `require_owner` (`src/core/dependencies.py`)
- [x] Structured exception hierarchy with FastAPI handlers (`src/core/exceptions.py`)
- [x] SKU/barcode generation, pagination utilities (`src/core/utils.py`)
- [x] FastAPI app factory with lifespan, CORS, health endpoint (`src/main.py`)
- [x] Vertical Slice Architecture folder structure (`src/features/`, `src/integrations/`)
- [x] All 12 ORM models across 7 feature slices
- [x] Alembic baseline migration (`001`) — 9 enums, 12 tables, all FK/check constraints, indexes
- [x] Second migration (`002`) — percent discount constraint + partial unique index on default address
- [x] `CLAUDE.md` with environment and architecture instructions

**Prerequisites — all complete ✅:**
- [x] `.env` file populated with real Neon DB URL, Neon Auth JWKS URL, and audience
- [x] `alembic upgrade head` run against the Neon database — all 12 tables live
- [x] `scripts/test_resend.py` created for manual email connection test
- [ ] USD pricing confirmed for all product lines — **still pending (blocking checkout)**
- [ ] Resend domain `vantierluxuryla.com` DNS verified — **pending (client action)**

---

### Phase 2 — Commerce Core (Backend API) ✅ COMPLETE

All slice files exist. Implementation order: **2.8 → 2.5 → 2.4 → 2.6 → 2.7**

> **Test suite:** 99 tests passing as of 2026-04-16. Run with:
> `pyenv exec python -m pytest -q`

#### 2.1 Products slice (`src/features/products/`) ✅ COMPLETE
- [x] Pydantic schemas: `ProductCreate`, `ProductUpdate`, `ProductResponse`, `VariantCreate`, `VariantResponse`
- [x] Service: product CRUD, variant CRUD, SKU auto-generation (margin validation moved to Frontend)
- [x] Router: `GET /products`, `POST /products`, `GET /products/{id}`, `PATCH /products/{id}`, variant sub-routes
- [x] Admin-only write endpoints (require `AdminUserDep`); public read endpoints

#### 2.2 Inventory slice (`src/features/inventory/`) ✅ COMPLETE
- [x] Schemas: `StockAdjustment`, `StockAdjustmentResponse`, `OperatingCostCreate`, `OperatingCostUpdate`, `OperatingCostResponse`
- [x] Service: stock adjustment (SELECT FOR UPDATE), low-stock alert per-variant (≤50 units → Resend email), barcode PDF generation (python-barcode + reportlab), OperatingCost CRUD
- [x] Router: `PATCH /inventory/variants/{id}/stock`, `GET /inventory/low-stock`, `GET /inventory/variants/{id}/barcode`, `POST/GET/PATCH/DELETE /inventory/operating-costs`
- [x] `resend_client.py`: `send_low_stock_alert()` bootstrap (fire-and-forget, never raises)
- [x] 16 tests passing

#### 2.3 Discounts slice (`src/features/discounts/`) ✅ COMPLETE
- [x] Schemas: `DiscountCodeCreate`, `DiscountCodeUpdate`, `DiscountCodeResponse`, `DiscountValidateRequest`, `DiscountValidateResponse`
- [x] Service: CRUD (case-insensitive dedup, uppercase normalization), margin-floor warning, usage count guard, expiry check, `increment_usage_count` (SELECT FOR UPDATE — called by Orders in 2.4)
- [x] Router: `POST /discounts`, `GET /discounts`, `GET /discounts/{id}`, `PATCH /discounts/{id}`, `POST /discounts/validate` (public)
- [x] 19 tests passing

---

#### 2.8 Users slice (`src/features/users/`) ✅ COMPLETE
- [x] Schemas: `AdminUserInvite`, `AdminUserResponse`, `AdminRoleUpdate`, `SelfRegisterRequest`
- [x] Service: list admins, deactivate (self-guard), role update (owner-only), bootstrap first owner
- [x] Router: `GET /users`, `POST /users/invite`, `PATCH /users/{id}`, `DELETE /users/{id}` (all Owner-only)
- [x] Seed script: `scripts/seed_owner.py` — creates first owner row from Neon Auth user ID
- [x] `scripts/auth_tool.py` — CLI sign-in/sign-up contra Neon Auth para obtener token (opaco) + intento de intercambio JWT
- [x] Auth bypass hardening: `ENABLE_DEV_AUTH=true` requerido explícitamente (no activo por defecto)
- [x] 6 tests de users en suite (71 total)

#### 2.5 Integrations (`src/integrations/`) ✅ COMPLETE
- [x] `resend_client.py`: all 6 triggers implemented (low_stock, order_confirmed, order_shipped, exchange_notification, new_order_alert, contact_form)
- [x] `stripe_client.py`: mock stub — real integration pending Stripe credentials from client
- [x] `envia_client.py`: mock stub — real integration pending envia.com credentials from client

#### 2.4 Orders slice (`src/features/orders/`) ✅ COMPLETE
- [x] Schemas: `OrderCreate`, `OrderItemCreate`, `OrderResponse`, `OrderStatusUpdate`, `CheckoutResponse`
- [x] Service: create_order, confirm_payment (webhook), get_order, get_order_for_user, list_orders, list_user_orders, update_order_status, generate_shipping_label
- [x] Router: `POST /checkout`, `POST /webhook/stripe`, `GET /my`, `GET /my/{id}`, `GET /` (admin), `GET /{id}` (admin), `PATCH /{id}/status`, `POST /{id}/shipping-label`

#### 2.6 Purchase Orders slice (`src/features/purchase_orders/`) ✅ COMPLETE
- [x] Schemas: `PurchaseOrderCreate`, `PurchaseOrderResponse`, `POStatusUpdate`, `POItemCreate`, `POItemResponse`
- [x] Service: list, get, create (variant validation + unique reference_number), update_po_status (ordered→in_transit|received, SELECT FOR UPDATE stock increment on received)
- [x] Router: `POST /purchase-orders`, `GET /purchase-orders`, `GET /purchase-orders/{id}`, `PATCH /purchase-orders/{id}/status` (all admin)
- [x] 7 tests passing

#### 2.7 Exchanges slice (`src/features/exchanges/`) ✅ COMPLETE
- [x] Schemas: `ExchangeCreate`, `ExchangeResponse`, `ExchangeAdminUpdate`
- [x] Service: create_exchange (order validation, variant-in-order check, duplicate guard, Resend fire-and-forget), update_exchange (same-line product validation), list, get
- [x] Router: `POST /exchanges` (authenticated), `GET /exchanges`, `GET /exchanges/{id}`, `PATCH /exchanges/{id}` (admin)
- [x] 7 tests passing

---

### Phase 3 — Storefront & Admin UI (Frontend) 🔄 IN PROGRESS

> **Session started 2026-04-17.** Auth wired, admin login functional, Cloudflare R2 connected, Inventory module live.

#### 3.0 Foundation ✅ COMPLETE
- [x] Vue 3 scaffold: Tailwind CSS v3, Pinia, Vue Router 4, Neon Auth SDK (`@neondatabase/auth`)
- [x] Vertical Slice Architecture in `frontend/src/features/`
- [x] Axios client with JWT interceptor (`shared/api/client.ts`) — baseURL `/api/v1`, auth header auto-injected
- [x] Route guard system (`shared/auth/guards.ts`) — `requireAdmin`, `requireOwner`, `requireAuth`, `guestOnly`
- [x] Auth store (`features/auth/store.ts`) — `login()`, `logout()`, `syncFromNeonAuth()`, `fetchRole()`
- [x] Neon Auth SDK client (`features/auth/auth-client.ts`)
- [x] LoginPage with redirect-to-dashboard after successful admin login
- [x] AdminLayout: collapsible sidebar, nav items, logout, real role badge
- [x] Infinite redirect loop bug fixed — 401 interceptor skips redirect when already on `/auth/*`
- [x] Auth is guest-only for customers — `/account`, `/orders`, `/exchanges` have no `requireAuth`
- [x] Cloudflare R2 integration — `cloudflare_client.py` + image upload endpoint on products router

#### 3.1 Admin — Inventory Module ✅ COMPLETE
- [x] `admin/inventory/types.ts` — `AdminProduct`, `AdminVariant`, payloads matching backend snake_case schema
- [x] `admin/inventory/api.ts` — full API layer: products CRUD, variants CRUD, stock adjust, low-stock, barcode URL, image upload
- [x] `admin/inventory/store.ts` — Pinia store with error handling and optimistic stock updates
- [x] `InventoryPage.vue` — real backend data, expandable variant rows, stock delta editing
- [x] Add Product modal (line, name, description) → `POST /api/v1/products`
- [x] Add Variant modal (style, size, color, price, cost, initial stock) → `POST /api/v1/products/:id/variants`
- [x] Image manager per variant → upload to Cloudflare R2 via `POST /api/v1/products/:id/variants/:id/images/upload`

#### 3.2 Admin — Dashboard
- [ ] Wire KPI cards to real backend data (revenue, orders, low stock, exchanges)
- [ ] Recent orders table from real `GET /api/v1/orders`

#### 3.3 Admin — Orders Module ✅ DISPLAY WORKING
- [x] List orders wired → `GET /api/v1/orders` (array→paginated adapter in frontend)
- [ ] Order detail modal → status update `PATCH /api/v1/orders/:id/status`
- [ ] Generate shipping label → `POST /api/v1/orders/:id/shipping-label`

#### 3.4 Admin — Discounts Module
- [ ] List, create, edit, disable discount codes → `/api/v1/discounts`
- [ ] Margin warning UI when discount breaks 50% floor

#### 3.5 Admin — Purchase Orders Module
- [ ] Create PO → `POST /api/v1/purchase-orders`
- [ ] Update status (ordered → in_transit → received) → stock auto-increments on receive

#### 3.6 Admin — Users Module
- [ ] List admins, invite by email, change role, deactivate → `/api/v1/users`

#### 3.7 Storefront — Homepage & Catalog
- [ ] Homepage components wired to real products (`FeaturedProducts`, `ProductLineGrid`)
- [ ] CatalogPage filters → `GET /api/v1/products?line=&size=&style=`
- [ ] ProductDetailPage images from Cloudflare R2 URLs

#### 3.8 Storefront — Cart & Checkout ✅ CORE FLOW COMPLETE
- [x] Cart Pinia store, free shipping banner (5+ items), discount code validation
- [x] Checkout: address form, shipping rate, Stripe Checkout Session redirect
- [x] `/checkout/success` + `/checkout/cancel` routes
- [x] Order confirmation screen + Resend HTML email (branded template, out of spam)
- [x] Image upload CORS fixed (multipart boundary issue)
- [x] Stripe webhook verified (WebhookSignature.verify_header, SDK v15 compatible)

#### 3.9 Storefront — Customer Account (optional, no registration required)
- [ ] Order lookup by email (guest-friendly)
- [ ] Exchange request form → `POST /api/v1/exchanges`

---

### Phase 4 — Financial Intelligence (Weeks 14–17)

- [ ] `financials` slice: profitability per product, revenue/COGS/margin aggregations
- [ ] Financial dashboard (Owner only): date-range filters, top SKUs, margin alerts
- [ ] Break-even simulation endpoint
- [ ] Revenue/expense CSV export

---

### Phase 5 — Polish & Launch (Weeks 18–24)

- [ ] Branding implementation (client-provided assets)
- [ ] Mobile responsiveness audit
- [ ] SEO meta tags + sitemap
- [ ] Performance optimization (LCP < 2.5s)
- [ ] Security audit (Stripe webhook sig, Neon Auth JWT, SQL injection, CORS)
- [ ] Staging environment QA
- [ ] Production deployment + DNS

---

## 12. Out of Scope (v1)

- Loyalty / rewards program
- Live chat / chatbot
- Blog / content marketing module
- Multi-warehouse support
- Automated restock from supplier (POs are manual)
- Social commerce (Instagram/TikTok Shop integration)
- Multi-currency display (USD only in v1)

---

## 13. Open Items / Decisions Needed

| # | Item | Owner | Status |
|---|---|---|---|
| 1 | Confirm USD pricing for all 3 lines × 2 styles | Vantier | ⛔ **Blocking Phase 2.4 checkout** |
| 2 | Provide brand assets: logo, color palette, fonts, photography | Vantier | Needed for Phase 3 |
| 3 | Confirm envia.com API credentials + account type | Vantier | ⛔ **Blocking 2.5 envia_client** |
| 4 | Confirm Stripe account (US entity or MX?) + credentials | Vantier | ⛔ **Blocking 2.5 stripe_client** |
| 5 | Confirm operating cost in USD (currently ~$580 MXN/order) | Vantier | Needed for margin calc |
| 6 | Define product color catalog per variant | Vantier | Needed for Phase 2 products |
| 7 | Verify `vantierluxuryla.com` domain DNS in Resend dashboard | Dev/Client | ✅ Verified 2026-04-18 — branded HTML emails confirmed delivered |
| 8 | Auth QA real — flujo completo end-to-end | Dev | ✅ Resuelto 2026-04-17 — bug `NEON_AUTH_AUDIENCE` corregido. Login → JWT (EdDSA) → `/users/me` → role `owner` → redirect `/admin/dashboard` funcional |
| 9 | Cloudflare R2 bucket conectado | Dev | ✅ Completo — `cloudflare_client.py`, upload de imágenes de producto en producción |

---

*PRD Version: 2.7 — April 2026*
*Stack: FastAPI · Neon PostgreSQL · Neon Auth · Resend · Stripe · envia.com · Vue 3 · Tailwind CSS · Cloudflare R2*
*Phase 1 complete. Phase 2 complete (99 tests, 49 routes). Phase 3 in progress — Stripe Checkout Sessions E2E verified, Resend HTML emails live, image uploads fixed, admin orders display working. Next: Admin Dashboard KPIs → Order detail/status → Discounts → Storefront catalog.*
