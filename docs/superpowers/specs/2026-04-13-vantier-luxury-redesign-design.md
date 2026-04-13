# Vantier — Luxury UX/UI Redesign

**Date:** 2026-04-13
**Stack:** Vue 3 + TypeScript + Tailwind CSS + Pinia
**Scope:** Homepage · Product Detail Page (PDP) · Catalog · Checkout polish

---

## 1. Design Direction

### Aesthetic: Silent Luxury / Editorial Atelier

Black nav + full-bleed editorial hero image + warm ivory body sections + black footer. No gradients between zones. Hard cuts between dark and light — architectural, intentional.

**Color palette (existing tokens.css):**
- Obsidian: `oklch(8% 0.005 250)` / `#0d0c0a` — nav, footer, hero, El Proceso section
- Ivory: `oklch(97% 0.003 90)` / `#faf9f6` — text on dark
- Warm Beige: `#f0ebe0` — body sections, product zones
- Amber/Gold: `oklch(78% 0.14 85)` / `rgba(200,169,110,*)` — accent lines, badges, Newsletter link. Never as background.

**Typography:**
- Display: Playfair Display, serif — product names, section titles, hero copy
- Body: Inter — labels, descriptions, UI elements
- All caps + wide letter-spacing for labels and nav items

**Image treatment:** All images and product cards — square corners, no border radius. Editorial, architectural.

**Micro-interaction tokens (existing):**
- `--ease-luxury: cubic-bezier(0.25, 0.1, 0.1, 1)`
- `--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1)`
- `--duration-cinematic: 600ms`

---

## 2. Homepage

### Scroll order (top → bottom):

1. **Announcement Bar** — black, full width. "Envío gratuito en compras mayores a $500 USD." Centered, 6px spaced-out uppercase.

2. **Nav** — black sticky. Left: VANTIER wordmark. Center: Home / Shop / About. Right: "Newsletter — 15% off" (gold, external redirect link) + cart icon (square border).

3. **Hero** — 380px full-bleed. Background: editorial photo (real image when available; CSS gradient placeholder during dev). CSS 3D multi-layer parallax on scroll:
   - Layer 1 (slow): dark background gradient
   - Layer 2 (medium): garment silhouette shape
   - Layer 3 (fast): text copy
   Copy bottom-left: collection label → display headline ("SILENT EVOLUTION.") → gold rule + subtitle → "Explore the Collection →" button (ghost border). Slide counter top-right (monospace). Gold progress bar bottom. 3 dot indicators.

4. **Shop by Line** — ivory `#f0ebe0`. Section header left ("The Collection") + "Ver todo →" right. 3-column grid, one column per garment line:
   - Polo Atelier — dark card `#1a1714`
   - Signature — mid beige `#c8bfac`
   - Essential — light ivory `#e8e2d5`
   Each card: 2:3 aspect ratio, gold corner accent line, category label + line name bottom-left. Hover: scale 1.02 + gold line extends + "Shop →" translates right.

5. **Brand Statement** — split panel. Left 38%: dark photo panel `#1a1714`, gold corner accent. Right: warm ivory `#f0ebe0`, founder quote italic, gold rule, "Silent Evolution." + "Timeless Legacy. Est. 2024", "Explorar la marca →" link. IntersectionObserver fade-up reveal on scroll.

6. **Selected Pieces** — warm beige `#ebe5d8`. Header "Selected Pieces" + "View all →". Grid: 3 product cards (3/4 aspect) + 1 editorial dark tile spanning wider ("Shop All →"). Product cards: scarcity badge "1 left" (ivory bg, gold border), product name gradient overlay bottom.

7. **El Proceso** — black `#0d0c0a`. 3-column grid, numbered 01/02/03, gold rule under each number. Columns: Diseño / Confección / Entrega. Each has a brief paragraph. Narrative: LA design, Mexico character, no shortcuts.

8. **Newsletter Strip** — warm beige `#ebe5d8`. "Únete al círculo Vantier" in Playfair. Subtitle. Single button (no input): "Unirme al círculo →" — external redirect to newsletter signup page for 15% discount.

9. **Footer** — black, symmetrical to nav. VANTIER wordmark left, links center, "Los Angeles — México" right. Gold rule divider. © 2025 Vantier.

---

## 3. Product Detail Page (PDP)

Each of the 3 garments (Polo Atelier / Signature / Essential) has the same structure with garment-specific content.

### Scroll order:

1. **Nav** (same as homepage, sticky)

2. **Breadcrumb** — black background. Shop → Line → Colorway. Gold accent on current item.

3. **Hero Split** — full-width, black background, min-height 480px:
   - Left 52%: product image zone. CSS 3D parallax layers (garment silhouette, depth shadow). Gold corner accent top-left. Thumbnail strip right side (3 thumbnails, square). "Zoom" hint bottom-center.
   - Right 48%: product info. Line label (gold) → Product name (Playfair, 22px) → Colorway subtitle → gold rule → Price + scarcity badge ("Solo X disponibles", amber border) → shipping note → color swatches (22px squares, selected has gold border) → size selector (square buttons, selected has gold border, sold-out has strikethrough) → size guide link → Primary CTA: "Agregar al carrito" (ivory bg, black text, full width) → Secondary CTA: "Comprar ahora" (ghost border) → product description paragraph.

4. **Lookbook** — warm ivory `#f0ebe0`. Section header "Lookbook". Two editorial photos side-by-side: main 3:2 large + portrait 2:3 smaller. Both square-cornered. "Ver lookbook completo →" button below (ghost border). Content populated when photo assets are available.

5. **Cómo cuidar tu prenda** — warm beige `#ebe5d8`. Section header. 4-column icon grid (square icon borders, text-based symbols): Lavado / Planchado / Almacenaje / Material. Each with instruction text. Closing note: gold rule + italic tagline about longevity.

6. **También te puede interesar** — warm ivory `#f0ebe0`. "De la misma línea" label + "También te puede interesar" title. 3-column grid: the other 2 garment lines + 1 editorial "Ver colección →" dark tile.

7. **Footer** (same as homepage)

---

## 4. Catalog Page

Grid of all product variants. Sidebar filters (desktop) / MobileFilterDrawer (mobile). Product cards: 3/4 aspect ratio, square corners, scarcity badge, color swatches, hover quick-add. Warm beige background.

No redesign changes to core catalog structure — apply design tokens (colors, typography, easing) to existing CatalogPage.vue component.

---

## 5. Checkout

3-step flow (Address → Shipping → Payment). Existing CheckoutStepper + OrderSummaryPanel structure retained.

Design token application: black stepper active state with gold accent, ivory form fields, Playfair for step titles. No structural changes.

---

## 6. Animations & Interactions

| Zone | Interaction | Implementation |
|------|-------------|----------------|
| Hero | Multi-layer parallax on scroll | CSS `transform: translateY()` via scroll listener, 3 layers at different speeds |
| BrandStatement | Fade-up reveal | `IntersectionObserver` (already scaffolded) |
| Category cards | Scale + gold line extend + Shop→ translate | CSS `transition` on hover |
| Nav | Sticky on scroll, transparent→black | `position: sticky`, existing scroll behavior |
| Product images | Zoom on hover | CSS `transform: scale(1.04)` with `overflow: hidden` |
| Size buttons | Selected state gold border | Pinia state + CSS class |
| Scarcity badge | Pulse animation if ≤2 units | CSS `@keyframes` subtle pulse |

---

## 7. Navigation — Newsletter Link

"Newsletter — 15% off" in nav is a standard `<a>` tag with `target="_blank"` pointing to external newsletter signup page. Gold color treatment `rgba(200,169,110,0.75)`. No backend required. No email input anywhere on the site — all newsletter interaction happens externally.

---

## 8. Inventory Strategy (3 Garments)

Vantier carries 3 main garment lines, each with color variants:
- **Polo Atelier** (Outerwear)
- **Signature** (Structured)
- **Essential** (Everyday)

Scarcity as luxury signal: low stock badges are always visible on cards and PDPs. "Solo X disponibles" in gold amber. XL or sold-out sizes shown with strikethrough, not hidden — scarcity is a feature, not a problem to hide.

---

## 9. Implementation Phases (Phased Approach C)

**Phase 1 — Homepage + Nav + Catalog tokens**
- StorefrontLayout.vue: nav redesign (black bg, gold Newsletter link)
- AnnouncementBar.vue: new component
- HeroCarousel.vue: parallax layers, editorial copy layout
- BrandStatement.vue: scroll reveal (already scaffolded)
- FeaturedProducts.vue: selected pieces grid
- New sections: ShopByLine, ElProceso, NewsletterStrip
- Apply design tokens to CatalogPage + ProductCard

**Phase 2 — PDP**
- ProductDetailPage.vue: hero split layout
- CSS 3D parallax on product image
- Lookbook section (placeholder until photo assets)
- CareInstructions component
- RelatedProducts component

**Phase 3 — Checkout polish**
- Apply design tokens to CheckoutPage, CheckoutStepper, StripePaymentForm
- Luxury form styling (ivory fields, gold focus ring, Playfair labels)

---

## 10. Out of Scope

- WebGL / Three.js / Spline — not in this redesign
- 3D product models — no assets available
- Newsletter backend — external redirect only
- New product lines beyond 3 existing
- Mobile app
