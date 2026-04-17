# Vantier — Admin Panel Complete Redesign

**Date:** 2026-04-17
**Stack:** Vue 3 + TypeScript + Tailwind CSS + Pinia
**Scope:** AdminLayout · Dashboard · Inventario · Órdenes · Compras · Descuentos · Financiero · Usuarios

---

## 1. Design Direction

### Aesthetic: Executive Minimalism

Soft cream background, pure white cards floating on depth shadows, deep gold/amber accent. No harsh borders — only very light grays or cream tones for separation. Rounded corners throughout (8px–12px). Clean sans-serif hierarchy.

### Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| `--admin-bg` | `#F9F7F2` | Page background (soft warm cream) |
| `--admin-card` | `#FFFFFF` | Cards, modals, sidebar sections |
| `--admin-card-shadow` | `0 1px 3px rgba(0,0,0,0.05), 0 4px 12px rgba(0,0,0,0.04)` | Card floating depth |
| `--admin-amber` | `#D4AF37` | Primary CTA, active nav, amber accents |
| `--admin-amber-08` | `rgba(212,175,55,0.08)` | Active nav background, product row tint |
| `--admin-amber-15` | `rgba(212,175,55,0.15)` | Hover on amber elements |
| `--admin-border` | `rgba(0,0,0,0.06)` | Subtle separators — no hard borders |
| `--admin-text-primary` | `#1A1714` | Primary text (obsidian) |
| `--admin-text-secondary` | `#8A857D` | Labels, subtitles, secondary info |
| `--admin-sidebar-bg` | `#0D0C0A` | Sidebar (obsidian — luxury contrast) |

### Status Colors (pastel, non-saturated)

| Estado | Background | Text | Usage |
|--------|-----------|------|-------|
| OK / Activo / Entregado | `#F0FAF4` | `#2D7A4F` | Healthy states |
| Bajo / En tránsito / Procesando | `#FDF7ED` | `#92600F` | Warning states |
| Crítico / Inactivo / Expirado | `#FEF2F2` | `#B91C1C` | Critical/error states |
| Enviado | `#F5F3FF` | `#6D28D9` | Shipping state |
| Pendiente | `#EFF6FF` | `#1D4ED8` | Pending/waiting state |
| Confirmada | `#F0FAF4` | `#2D7A4F` | Confirmed PO |
| Recibida | `#F5F3FF` | `#6D28D9` | Received PO |

### Typography (Inter — already installed)

| Role | Size | Weight | Transform |
|------|------|--------|-----------|
| Page title | `1.5rem` | `700` | — |
| Section title | `1rem` | `600` | — |
| KPI value | `2.25rem` | `700` | — |
| Table header label | `0.65rem` | `600` | uppercase + tracking-wider |
| Table cell body | `0.875rem` | `400` | — |
| Nav item | `0.75rem` | `500` | uppercase + tracking-widest |
| Group label (sidebar) | `0.6rem` | `600` | uppercase + tracking-widest |

---

## 2. AdminLayout (Sidebar + Topbar)

### Sidebar (240px, obsidian `#0D0C0A`)

**Brand zone (top, 64px):**
- VANTIER wordmark: ivory, `font-weight: 700`, `letter-spacing: 0.2em`, `11px`
- Subtitle "PANEL ADMINISTRATIVO": amber `#D4AF37`, `9px`, uppercase, tracking-widest
- Divider: `border-bottom: 1px solid rgba(255,255,255,0.08)`

**Nav groups:**
```
PRINCIPAL
  Dashboard
  Inventario     [badge: count]

OPERACIONES
  Órdenes        [badge: count]
  Compras

FINANZAS
  Descuentos
  Financiero

SISTEMA
  Usuarios
```

Group label: `rgba(255,255,255,0.2)`, `0.6rem`, uppercase, `letter-spacing: 0.15em`, `padding: 16px 16px 6px`

**Nav item states:**
- **Active:** `border-left: 3px solid #D4AF37`, text `#D4AF37`, bg `rgba(212,175,55,0.08)`
- **Inactive:** text `rgba(255,255,255,0.5)`, hover → `rgba(255,255,255,0.8)` + `rgba(255,255,255,0.05)` bg
- **Badge:** pill `#D4AF37` bg, obsidian text, `8px` font, `px-1.5 py-0.5`, `border-radius: 999px`

**User card (bottom, above footer):**
- Divider `rgba(255,255,255,0.08)`
- Avatar circle: initials, amber bg
- Name: ivory, `0.875rem`, `font-weight: 500`
- Role: amber, `0.65rem`, uppercase
- "Cerrar sesión" button: `rgba(255,255,255,0.4)`, hover `rgba(255,255,255,0.7)`
- "Ver tienda →" link: same subdued style

Sidebar has collapse toggle (chevron icon) → collapses to 64px icon-only mode.

### Topbar (60px, white card, shadow `0 1px 0 rgba(0,0,0,0.06)`)

**Left:** Page title (`font-weight: 700, 1.1rem`) + breadcrumb path (`text-secondary, 0.8rem`, separated by `·`)

**Right:** Search icon + Notifications bell (with count badge if >0) + User avatar (circular, 32px)

All topbar icons: `#8A857D` at rest, `#D4AF37` on hover.

---

## 3. Shared Components

### `AdminStatCard`

```
┌────────────────────────────────────────┐  border-radius: 12px
│ [icon 20px amber]      TOTAL SKUS      │  label: 0.65rem, uppercase, #8A857D
│                                        │
│   48                                   │  value: 2.25rem, weight 700, #1A1714
│   en 12 productos          [+8% ↑]     │  sub: 0.75rem, #8A857D | delta: pastel pill
└────────────────────────────────────────┘
```
- Background: `#FFFFFF`, shadow: `--admin-card-shadow`
- Delta badge: green pastel if positive, red pastel if negative
- Icon: SVG outline, 20px, color `#D4AF37`
- `padding: 20px 24px`

### `StatusBadge`

Pill-shaped span. `border-radius: 999px`, `padding: 2px 10px`, `font-size: 0.7rem`, `font-weight: 500`.

Includes a 6px filled dot before the text. Uses pastel colors from Section 1 table.

Props: `status: 'ok' | 'bajo' | 'critico' | 'activo' | 'inactivo' | 'expirado' | 'pendiente' | 'procesando' | 'enviado' | 'entregado' | 'confirmada' | 'recibida' | 'en_transito'`

Label map (Spanish):
- `ok` → "OK"
- `bajo` → "Bajo"  
- `critico` → "Crítico"
- `activo` → "Activo"
- `inactivo` → "Inactivo"
- `expirado` → "Expirado"
- `pendiente` → "Pendiente"
- `procesando` → "Procesando"
- `enviado` → "Enviado"
- `entregado` → "Entregado"
- `confirmada` → "Confirmada"
- `recibida` → "Recibida"
- `en_transito` → "En tránsito"

### `StockBar`

Thin progress bar (4px height, `border-radius: 2px`).

Props: `current: number, threshold: number` (threshold = "full" reference, default 50).

Color logic based on `current / threshold * 100`:
- `> 30%` → green `#2D7A4F`
- `10–30%` → amber `#D4AF37`
- `< 10%` → red `#B91C1C`

Bar fill capped at 100%. Shows stock number `84 uds` to the right in `0.75rem text-secondary`.

Inventory page passes `threshold=50` so ≤5 uds maps to Crítico and ≤15 uds maps to Bajo naturally.

### `AdminTable`

- No visible grid. Row separator: `border-bottom: 1px solid rgba(0,0,0,0.04)`
- Header row: `background: #F9F7F2`, labels uppercase 0.65rem, weight 600, `#8A857D`
- Body row hover: `background: rgba(0,0,0,0.015)`
- Product group rows: `background: rgba(212,175,55,0.04)`, text weight 600
- Rounded container: `border-radius: 12px`, overflow hidden

### `AdminButton`

- **Primary:** `background: #D4AF37`, text `#FFFFFF`, `border-radius: 8px`, `padding: 8px 16px`, `font-size: 0.8rem`, uppercase, tracking-wider. Hover: `brightness(0.92)`.
- **Ghost:** `border: 1px solid #D4AF37`, text `#D4AF37`, transparent bg. Hover: `background: rgba(212,175,55,0.08)`.
- **Danger:** `border: 1px solid #F87171`, text `#B91C1C`. Hover: `background: #FEF2F2`.

### `AdminFilterBar`

Horizontal flex row, `gap: 12px`.

- **Search input:** `border-radius: 8px`, `border: 1px solid rgba(0,0,0,0.1)`, `background: #FFFFFF`, magnifier icon inside left, `padding: 8px 12px 8px 36px`, focus ring `#D4AF37 1px`.
- **Dropdowns:** same border/radius style, trailing chevron icon, `min-width: 140px`.
- Sits on `#F9F7F2` background — no container card, fully integrated.

### `MarginHealthBar`

For Descuentos only. Horizontal bar, 6px height, `border-radius: 3px`.
- `> 60%` margin → green
- `40–60%` → amber
- `< 40%` → red, + discrete alert chip below: `⚠ Margen bajo` in red pastel pill

---

## 4. Pages

### Dashboard (`/admin/dashboard`)

**Layout:** page header → 4 stat cards → recent orders table → quick actions

**Stat cards (4, grid 2-col on md / 4-col on xl):**
1. Revenue Hoy — `$3,240` · `18 órdenes` · delta `+12%`
2. Órdenes este mes — `342` · `$58,400 total` · delta `+8%`
3. Stock Bajo — `7` · `variantes ≤ 5 uds` · delta `+3` (negative)
4. Exchanges Pendientes — `4` · `pendientes aprobación` · delta `-2` (positive)

**Órdenes Recientes table (7 rows max):**
Columns: `ORDEN · CLIENTE · ITEMS · TOTAL · ESTADO · FECHA`
`StatusBadge` in Estado column with full Spanish label.

**Quick Actions (3 ghost buttons):**
`+ Agregar Producto` (primary) · `Ver Órdenes` (ghost) · `Crear Descuento` (ghost)

---

### Inventario (`/admin/inventory`)

**Stat cards (5, horizontally scrollable on mobile):**
1. Total SKUs — icon: briefcase amber
2. Stock Total — icon: cube amber
3. Stock Bajo — icon: warning amber, value in red if >0
4. Valor Inventario — icon: dollar amber, `$86.4k`
5. Imágenes — icon: image amber, `34 · Cloudflare R2`

**Filter bar:** búsqueda + "Todas las líneas" + "Todo el stock"

**Table structure:**

```
PRODUCTO / VARIANTE | SKU | TALLA | COLOR | PRECIO | COSTO | STOCK | ESTADO | ACCIONES
────────────────────────────────────────────────────────────────────────────────────────
▶ Varsovia          |     |       |       |        |       | 3 variantes · Linea A     [+]
  └ Varsovia        | VRS-NGR-M | M | Negro | $185 | $72 | [████░░] 12 uds | [Bajo]  | ✏ 📊
  └ Varsovia        | VRS-BEI-L | L | Beige | $185 | $72 | [████████] 84   | [OK]    | ✏ 📊
▶ Ginebra           |     |       |       |        |       | 4 variantes · Linea B     [+]
  └ Ginebra         | GNB-BLN-S | S | Blanco| $210 | $85 | [█░░░░░░]  5   | [Crítico]| ✏ 📊
```

- Product rows: `background: rgba(212,175,55,0.04)`, collapse toggle chevron
- Variant rows: white bg, `StockBar` in stock column, `StatusBadge` in estado column
- Stock threshold: ≤5 → Crítico (red), ≤15 → Bajo (amber), >15 → OK (green)
- Actions: edit icon + trend icon, `#8A857D` at rest → `#D4AF37` on hover

**Buttons:** `+ Variante` (ghost) + `+ Nuevo Producto` (primary) — top right header

**Modals:** Add Product, Add Variant, Image Manager — white card, `border-radius: 16px`, backdrop blur

---

### Órdenes (`/admin/orders`)

**Stat cards (3):**
1. Pendientes — count
2. En Proceso — count
3. Enviadas — count

**Table columns:** `ORDEN · CLIENTE · ARTÍCULOS · TOTAL · ESTADO · FECHA · ACCIONES`

**Actions column:** eye icon (view detail) + `StatusBadge`.

Order detail: slide-in panel (right side) or modal with full order breakdown.

---

### Compras (`/admin/purchases`)

**Stat cards (2):**
1. POs Activas — count
2. Valor en Tránsito — `$XX,XXX`

**Table columns:** `# PO · PROVEEDOR · ARTÍCULOS · TOTAL · ESTADO · FECHA ESPERADA · ACCIONES`

Status badges: Confirmada (green) / En tránsito (amber) / Recibida (purple).

**Button:** `+ Nueva OC` (primary amber) — top right.

---

### Descuentos (`/admin/discounts`)

**Layout:** stats row → coupon card grid (2–3 col)

**Stat cards (2):**
1. Cupones Activos — count
2. Descuento Promedio — `XX%`

**Coupon card structure:**
```
┌─────────────────────────────────────────┐
│ VANTIER20                 [Activo]       │  ← code monospace bold + StatusBadge
│ 20% descuento · Válido hasta 31/12/2025 │  ← type + expiry, text-secondary
│                                         │
│ Usos                          45 / 100  │  ← label + fraction
│ [████████████░░░░░░░░░░░░░░░░░░░░░░░░░] │  ← UsageBar (amber)
│                                         │
│ Margen Actual                     62%   │
│ [██████████████████░░░░░░░░░░░░░░░░░░░] │  ← MarginHealthBar
│                                         │
│ ⚠ Margen por debajo del 50%            │  ← only shown if margin < 50%, red pastel chip
└─────────────────────────────────────────┘
```

Card: white, `border-radius: 12px`, shadow. Monospace code in primary text.

**Button:** `+ Nuevo Cupón` (primary amber) — top right.

---

### Financiero (`/admin/financials`)

**Stat cards (4):**
1. Revenue Total — period
2. Costo Total — period
3. Margen Bruto — `XX%`
4. Órdenes Pagadas — count

**Transactions table columns:** `TIPO · DESCRIPCIÓN · ORDEN REF · MONTO · FECHA`

- Tipo column: small icon — arrow-up green (ingreso) / arrow-down red (egreso)
- Monto: green text for ingreso, red for egreso

---

### Usuarios (`/admin/users`)

**Table columns:** `USUARIO · EMAIL · ROL · REGISTRO · ACCIONES`

- Usuario: avatar circle with initials + name
- Rol: `StatusBadge` style — Owner (amber tint), Admin (blue pastel), Customer (gray)
- Actions: edit icon

---

## 5. Animations & Interactions

| Element | Interaction | Implementation |
|---------|-------------|----------------|
| Sidebar nav item | Active border slide-in | CSS transition on border-left |
| Stat card | Subtle scale on hover | `transform: scale(1.01)`, `transition: 150ms` |
| Table row | Soft bg fade on hover | `transition: background 150ms` |
| Product group row | Expand/collapse variants | `max-height` transition, `overflow: hidden` |
| Modal | Fade + scale in | `opacity` + `transform: scale(0.97→1)`, `150ms` |
| StockBar | Fill on mount | `width` transition from 0 to value, `600ms ease-out` |
| Admin buttons | Brightness on hover | CSS `filter: brightness()` |

---

## 6. File Structure

```
frontend/src/
├── pages/
│   └── AdminLayout.vue              ← full redesign
│
├── features/admin/
│   ├── components/shared/
│   │   ├── AdminStatCard.vue        ← new shared component
│   │   ├── StatusBadge.vue          ← new shared component
│   │   ├── StockBar.vue             ← new shared component
│   │   ├── AdminTable.vue           ← new shared component (optional wrapper)
│   │   ├── AdminButton.vue          ← new shared component
│   │   ├── AdminFilterBar.vue       ← new shared component
│   │   └── MarginHealthBar.vue      ← new shared component (Discounts only)
│   │
│   ├── dashboard/components/DashboardPage.vue   ← redesign
│   ├── inventory/components/InventoryPage.vue   ← redesign
│   ├── orders/components/OrdersPage.vue         ← redesign
│   ├── purchases/components/PurchasesPage.vue   ← redesign
│   ├── discounts/components/DiscountsPage.vue   ← redesign
│   ├── financials/components/FinancialsPage.vue ← redesign
│   └── users/components/UsersPage.vue           ← redesign
```

---

## 7. CSS Variables Extension

Add to existing `tokens.css` (or a new `admin-tokens.css` imported in `AdminLayout.vue`):

```css
:root {
  --admin-bg: #F9F7F2;
  --admin-card: #FFFFFF;
  --admin-card-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 4px 12px rgba(0,0,0,0.04);
  --admin-amber: #D4AF37;
  --admin-amber-08: rgba(212,175,55,0.08);
  --admin-amber-15: rgba(212,175,55,0.15);
  --admin-border: rgba(0,0,0,0.06);
  --admin-text-primary: #1A1714;
  --admin-text-secondary: #8A857D;
  --admin-sidebar-bg: #0D0C0A;

  /* Status colors */
  --status-ok-bg: #F0FAF4;
  --status-ok-text: #2D7A4F;
  --status-warn-bg: #FDF7ED;
  --status-warn-text: #92600F;
  --status-crit-bg: #FEF2F2;
  --status-crit-text: #B91C1C;
  --status-ship-bg: #F5F3FF;
  --status-ship-text: #6D28D9;
  --status-pend-bg: #EFF6FF;
  --status-pend-text: #1D4ED8;
}
```

---

## 8. Out of Scope

- Charts/graphs (revenue trend lines) — not in this redesign
- Mobile responsive admin — desktop-first only
- Real-time notifications — bell icon is visual only
- Dark mode for admin panel
- New backend endpoints — all pages use existing API contracts
