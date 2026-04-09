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

> **Note:** MXN reference prices are in the document. Client must confirm USD pricing before development of the checkout module.

### 3.2 Product Variants
Each SKU is defined by: **Line × Style (Classic/Design) × Size × Color**
The system auto-generates unique barcodes/SKUs for each variant, printable from the admin panel.

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
- **Auth:** Clerk account (email/social login)

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
- Profit margin alert: visual warning when any product's effective margin < 50%

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
- Types: % off, fixed amount off
- System validation: discount cannot reduce margin below 50% floor (alert shown)
- Usage limit and expiration date per code

#### User Management
- Two roles: Owner, Operative
- Invite team members by email (Clerk)
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
| Authentication | **Clerk** (JWT verification middleware) |
| Email | **Resend** (transactional via REST API) |
| Payments | **Stripe** (Checkout Sessions + Webhooks) |
| Shipping | **envia.com API** (rate calculation + label generation) |
| Barcode Gen | `python-barcode` + `qrcode` |
| PDF Labels | `reportlab` or `WeasyPrint` |

### Frontend
| Layer | Technology |
|---|---|
| Framework | **Vue.js 3** (Composition API) |
| Styling | **Tailwind CSS v3** |
| State | **Pinia** |
| Routing | **Vue Router 4** |
| Auth UI | **Clerk Vue SDK** |
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

## 9. Data Model (High-Level)

```
users (Clerk user_id, role: owner|operative, email)

products (id, line: polo_atelier|signature|essential, name, description, style: classic|design)

product_variants (id, product_id, size, color, sku, barcode, stock_qty, cost_acquisition_usd, images[])

orders (id, customer_clerk_id, status, subtotal_usd, shipping_usd, discount_usd, total_usd, shipping_address, stripe_payment_intent_id, carrier_tracking_number, envia_label_url)

order_items (id, order_id, variant_id, qty, unit_price_usd)

discount_codes (id, code, type: percent|fixed, value, usage_limit, expires_at, is_active)

exchanges (id, order_id, original_variant_id, replacement_variant_id, status, notes)

purchase_orders (id, supplier_name, expected_arrival, status: ordered|in_transit|received)

purchase_order_items (id, po_id, variant_id, qty_ordered, qty_received)

operating_costs (id, label, amount_usd, is_recurring)
```

---

## 10. Business Logic & Policies

### Shipping
- Real-time rate from envia.com API using fixed dimensions 33×26×10 cm
- Free shipping automatically applied when `order_items.count >= 5`
- International shipping supported (envia.com covers cross-border from Mexico)

### Pricing & Margins
- All prices stored and displayed in USD
- Margin formula: `(sale_price − cost_acquisition − operating_costs) / sale_price ≥ 0.50`
- Discount codes validated server-side; rejected if margin floor breached
- Financial dashboard shows: revenue, COGS, operating costs, net profit, margin %

### Exchanges (no returns)
- Customer initiates via account portal or contact form
- Same product line/category only
- Admin logs exchange in system; shipping cost covered by Vantier
- Resend triggers notification emails to both parties

### Barcodes / SKUs
- Auto-generated on variant creation: format `VAT-{LINE}-{STYLE}-{SIZE}-{COLOR}-{SEQUENCE}`
- Printable as PDF barcode label from admin panel

---

## 11. Development Roadmap (3–6 months)

### Phase 1 — Foundation (Weeks 1–4)
- [ ] Project scaffolding: FastAPI + Vue 3 + Tailwind + Neon DB
- [ ] Clerk auth integration (storefront + admin)
- [ ] Database schema + Alembic migrations
- [ ] Product CRUD API + admin UI
- [ ] Product variant management + barcode generation
- [ ] Basic storefront: homepage, catalog, PDP

### Phase 2 — Commerce Core (Weeks 5–9)
- [ ] Cart + checkout flow
- [ ] Stripe integration (payment sessions + webhooks)
- [ ] envia.com shipping rate API integration
- [ ] Free shipping logic (5+ items)
- [ ] Discount code system (with margin validation)
- [ ] Order management in admin

### Phase 3 — Operations (Weeks 10–13)
- [ ] Resend email notifications (all triggers)
- [ ] Shipping label generation (envia.com)
- [ ] Purchase orders module
- [ ] Stock alert system
- [ ] Exchange request flow

### Phase 4 — Financial Intelligence (Weeks 14–17)
- [ ] Financial dashboard (Owner role)
- [ ] Real-time profitability per product
- [ ] Margin alert system
- [ ] Break-even simulation tool
- [ ] Revenue/expense CSV export

### Phase 5 — Polish & Launch (Weeks 18–24)
- [ ] Branding implementation (client-provided assets)
- [ ] Mobile responsiveness audit
- [ ] SEO meta tags + sitemap
- [ ] Performance optimization (LCP < 2.5s)
- [ ] Security audit (Stripe webhook sig, Clerk JWT, SQL injection, CORS)
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

| # | Item | Owner |
|---|---|---|
| 1 | Confirm USD pricing for all 3 lines × 2 styles | Vantier |
| 2 | Provide brand assets: logo, color palette, fonts, photography | Vantier |
| 3 | Confirm envia.com API credentials + account type | Vantier |
| 4 | Confirm Stripe account (US entity or MX?) for payout currency | Vantier |
| 5 | Confirm operating cost in USD (currently documented as ~$580 MXN) | Vantier |
| 6 | Define product color catalog per variant | Vantier |

---

*PRD Version: 1.0 — April 2026*
*Stack: FastAPI · Neon PostgreSQL · Clerk · Resend · Stripe · envia.com · Vue 3 · Tailwind CSS*
