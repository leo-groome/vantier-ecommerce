# Vantier Luxury UX/UI Redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign the Vantier storefront with a Silent Luxury aesthetic — black nav/footer, editorial hero with CSS parallax, warm ivory content sections, and per-garment PDP storytelling (lookbook + care instructions + related products).

**Architecture:** Three phases executed sequentially. Phase 1 rebuilds the homepage shell and nav. Phase 2 adds PDP storytelling sections below the existing product hero. Phase 3 applies design tokens to the checkout flow. All changes are pure Vue/Tailwind — no new dependencies required.

**Tech Stack:** Vue 3 + TypeScript + Tailwind CSS + Pinia · Vitest + @vue/test-utils (jsdom) · Existing design tokens in `frontend/src/styles/tokens.css`

---

## File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `frontend/src/pages/StorefrontLayout.vue` | Modify | Nav → black bg, Newsletter gold external link |
| `frontend/src/features/home/pages/HomePage.vue` | Modify | Wire new sections, correct order |
| `frontend/src/features/home/components/HeroCarousel.vue` | Modify | CSS parallax scroll layers |
| `frontend/src/features/home/components/BrandStatement.vue` | Modify | Text panel bg → `var(--color-warm-beige)` |
| `frontend/src/features/home/components/ElProceso.vue` | **Create** | 3-step process section (homepage) |
| `frontend/src/features/home/components/NewsletterStrip.vue` | **Create** | External newsletter CTA strip |
| `frontend/src/shared/components/AppFooter.vue` | Modify | Replace email form with external link |
| `frontend/src/features/products/components/ProductDetailPage.vue` | Modify | Mount PDP storytelling sections |
| `frontend/src/features/products/components/ProductLookbook.vue` | **Create** | Lookbook editorial photos section |
| `frontend/src/features/products/components/CareInstructions.vue` | **Create** | Garment-specific care icons section |
| `frontend/src/features/products/components/RelatedProducts.vue` | **Create** | "También te puede interesar" cross-sell |
| `frontend/src/features/home/components/__tests__/ElProceso.test.ts` | **Create** | Unit tests |
| `frontend/src/features/home/components/__tests__/NewsletterStrip.test.ts` | **Create** | Unit tests |
| `frontend/src/features/products/components/__tests__/CareInstructions.test.ts` | **Create** | Unit tests |
| `frontend/src/features/products/components/__tests__/RelatedProducts.test.ts` | **Create** | Unit tests |

---

## Phase 1 — Homepage & Nav

---

### Task 1: Nav → Black Background + Newsletter Link

**Files:**
- Modify: `frontend/src/pages/StorefrontLayout.vue`

- [ ] **Step 1: Change nav background to Obsidian**

In `StorefrontLayout.vue`, find the `<header>` element and replace its classes:

```html
<!-- BEFORE -->
<header class="sticky top-0 z-40 border-b border-[color:var(--color-border)] bg-[color:var(--color-surface)]/95 backdrop-blur-sm">

<!-- AFTER -->
<header class="sticky top-0 z-40 border-b border-[color:var(--color-amber-accent)]/8 bg-[color:var(--color-obsidian)]">
```

- [ ] **Step 2: Change logo text color to Ivory**

```html
<!-- BEFORE -->
class="text-[length:var(--text-small)] font-bold uppercase tracking-[var(--tracking-display)] text-[color:var(--color-on-surface)] hover:opacity-70 transition-opacity duration-[var(--duration-fast)]"

<!-- AFTER -->
class="text-[length:var(--text-small)] font-bold uppercase tracking-[var(--tracking-display)] text-[color:var(--color-ivory)] hover:opacity-70 transition-opacity duration-[var(--duration-fast)]"
```

- [ ] **Step 3: Change nav link colors to Ivory + add Newsletter link**

Replace the entire `<nav>` desktop block and `<!-- Right actions -->` div:

```html
<!-- Desktop nav links -->
<nav class="hidden md:flex items-center gap-8" aria-label="Main navigation">
  <RouterLink
    v-for="link in navLinks"
    :key="link.to"
    :to="link.to"
    class="text-[length:var(--text-small)] font-medium uppercase tracking-[var(--tracking-label)] text-[color:var(--color-ivory)]/50 hover:text-[color:var(--color-ivory)] relative after:absolute after:bottom-0 after:left-0 after:h-px after:bg-[color:var(--color-ivory)] after:transition-[width] after:duration-[var(--duration-normal)] after:ease-[var(--ease-out-expo)] hover:after:w-full transition-colors duration-[var(--duration-fast)]"
    :class="$route.path === link.to ? 'text-[color:var(--color-ivory)] after:w-full' : 'after:w-0'"
  >
    {{ link.label }}
  </RouterLink>
</nav>

<!-- Right actions -->
<div class="flex items-center gap-4">
  <!-- Newsletter external link -->
  <a
    :href="newsletterUrl"
    target="_blank"
    rel="noopener noreferrer"
    class="hidden md:inline-flex text-[length:var(--text-small)] font-medium uppercase tracking-[var(--tracking-label)] text-[color:var(--color-amber-accent)]/80 hover:text-[color:var(--color-amber-accent)] border-b border-[color:var(--color-amber-accent)]/30 hover:border-[color:var(--color-amber-accent)] pb-px transition-all duration-[var(--duration-fast)]"
  >
    Newsletter — 15% off
  </a>

  <!-- Cart icon -->
  <button class="relative p-2 hover:opacity-70 transition-opacity duration-[var(--duration-fast)] text-[color:var(--color-ivory)]" aria-label="Open cart" @click="cartOpen = true">
    <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/>
    </svg>
    <Transition name="badge-pop">
      <span
        v-if="cart.totalItems > 0"
        :key="cart.totalItems"
        class="absolute -top-0.5 -right-0.5 w-4 h-4 bg-[color:var(--color-amber-accent)] text-[color:var(--color-obsidian)] text-[10px] font-bold flex items-center justify-center"
      >
        {{ cart.totalItems > 9 ? '9+' : cart.totalItems }}
      </span>
    </Transition>
  </button>

  <!-- Hamburger (mobile only) -->
  <button
    class="md:hidden p-2 hover:opacity-70 transition-opacity duration-[var(--duration-fast)] text-[color:var(--color-ivory)]"
    :aria-label="mobileMenuOpen ? 'Close menu' : 'Open menu'"
    :aria-expanded="mobileMenuOpen"
    @click="mobileMenuOpen = !mobileMenuOpen"
  >
    <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <Transition name="hamburger" mode="out-in">
        <g v-if="!mobileMenuOpen" key="open">
          <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>
        </g>
        <g v-else key="close">
          <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
        </g>
      </Transition>
    </svg>
  </button>
</div>
```

- [ ] **Step 4: Add newsletterUrl ref and fix mobile menu colors**

In the `<script setup>` block, add:

```ts
const newsletterUrl = 'https://vantierluxuryla.com/newsletter' // replace with real URL when known
```

Fix the mobile menu overlay background and text:

```html
<!-- Mobile menu overlay -->
<Transition name="mobile-menu">
  <nav
    v-if="mobileMenuOpen"
    class="md:hidden border-t border-[color:var(--color-amber-accent)]/10 bg-[color:var(--color-obsidian)] px-[var(--spacing-container)] py-6 flex flex-col gap-5"
    aria-label="Mobile navigation"
  >
    <RouterLink
      v-for="link in navLinks"
      :key="link.to"
      :to="link.to"
      class="text-[length:var(--text-title)] font-light uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-ivory)] hover:opacity-60 transition-opacity duration-[var(--duration-fast)]"
      :class="{ 'opacity-40': $route.path !== link.to }"
    >
      {{ link.label }}
    </RouterLink>
    <a
      :href="newsletterUrl"
      target="_blank"
      rel="noopener noreferrer"
      class="text-[length:var(--text-title)] font-light uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-amber-accent)]/70"
    >
      Newsletter — 15% off
    </a>
  </nav>
</Transition>
```

- [ ] **Step 5: Verify in browser**

Run: `cd frontend && npm run dev`

Open http://localhost:5173. Confirm:
- Nav is solid black
- VANTIER wordmark is white
- Nav links are white/dimmed
- "Newsletter — 15% off" shows in gold on the right
- Cart badge is gold on black
- Mobile hamburger opens a black overlay with the newsletter link

- [ ] **Step 6: Commit**

```bash
git add frontend/src/pages/StorefrontLayout.vue
git commit -m "feat(nav): black obsidian background, ivory links, gold newsletter CTA"
```

---

### Task 2: HeroCarousel — CSS Parallax Scroll

**Files:**
- Modify: `frontend/src/features/home/components/HeroCarousel.vue`

- [ ] **Step 1: Add scroll state and listener to script setup**

Add after the existing `onUnmounted` import line:

```ts
import { ref, onMounted, onUnmounted } from 'vue'

// existing slides array stays unchanged ...

const scrollY = ref(0)

function onScroll() {
  scrollY.value = window.scrollY
}
```

In `onMounted`, add the scroll listener alongside the timer:

```ts
onMounted(() => {
  timer = setInterval(() => { current.value = (current.value + 1) % slides.length }, 6000)
  window.addEventListener('scroll', onScroll, { passive: true })
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
  window.removeEventListener('scroll', onScroll)
})
```

- [ ] **Step 2: Apply parallax transform to hero background image**

In the template, find the background photo `<img>` and add a dynamic `:style`:

```html
<!-- Background photo -->
<img
  v-if="slide.image"
  :src="slide.image"
  :alt="slide.sub"
  class="absolute inset-0 w-full h-full object-cover pointer-events-none"
  :class="slide.dark ? 'opacity-60' : 'opacity-45'"
  :style="{ transform: `translateY(${scrollY * 0.35}px)` }"
/>
```

The image moves up at 35% of scroll speed — slower than the page = parallax depth effect.

- [ ] **Step 3: Apply subtle drift to hero text content**

Find the `<!-- Content -->` div and add `:style`:

```html
<!-- Content -->
<div
  class="relative z-10 pb-20 px-[var(--spacing-container)] max-w-[var(--container-max)] mx-auto w-full"
  :style="{
    transform: `translateY(${scrollY * 0.12}px)`,
    opacity: Math.max(0, 1 - scrollY / 380),
  }"
>
```

Text drifts up slightly and fades as user scrolls past the hero. `380` matches the hero height in px.

- [ ] **Step 4: Ensure hero section clips overflow from extended image**

The section already has `overflow-hidden` — confirm it's present:

```html
<section class="relative w-full h-[90vh] min-h-[560px] overflow-hidden select-none">
```

If missing, add `overflow-hidden`.

- [ ] **Step 5: Verify in browser**

Scroll slowly past the hero. The background image should move up slower than the page scroll. Text should fade out as it exits view. No layout shifts.

- [ ] **Step 6: Commit**

```bash
git add frontend/src/features/home/components/HeroCarousel.vue
git commit -m "feat(hero): CSS parallax — image layer 35%, text drift 12% with fade"
```

---

### Task 3: BrandStatement — Warm Beige Text Panel

**Files:**
- Modify: `frontend/src/features/home/components/BrandStatement.vue`

- [ ] **Step 1: Change text panel background to warm beige**

Find the right text panel div and replace `bg-[color:var(--color-ivory)]` with `bg-[color:var(--color-warm-beige)]`:

```html
<!-- BEFORE -->
<div
  class="md:basis-3/5 bg-[color:var(--color-ivory)] flex flex-col justify-center px-10 md:px-16 py-16 md:py-20"

<!-- AFTER -->
<div
  class="md:basis-3/5 bg-[color:var(--color-warm-beige)] flex flex-col justify-center px-10 md:px-16 py-16 md:py-20"
```

- [ ] **Step 2: Verify in browser**

The brand statement text panel should now show warm ivory (`#f0ebe0`) instead of pure white. The dark photo left + warm beige right contrast should feel editorial.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/features/home/components/BrandStatement.vue
git commit -m "feat(brand-statement): warm beige text panel bg for editorial warmth"
```

---

### Task 4: ElProceso Component

**Files:**
- Create: `frontend/src/features/home/components/ElProceso.vue`
- Create: `frontend/src/features/home/components/__tests__/ElProceso.test.ts`

- [ ] **Step 1: Write the failing test**

Create `frontend/src/features/home/components/__tests__/ElProceso.test.ts`:

```ts
import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import ElProceso from '../ElProceso.vue'

describe('ElProceso', () => {
  it('renders 3 steps', () => {
    const wrapper = mount(ElProceso)
    expect(wrapper.findAll('[data-step]')).toHaveLength(3)
  })

  it('renders step numbers 01, 02, 03', () => {
    const wrapper = mount(ElProceso)
    const numbers = wrapper.findAll('[data-step-number]').map(el => el.text())
    expect(numbers).toEqual(['01', '02', '03'])
  })

  it('renders step titles Diseño, Confección, Entrega', () => {
    const wrapper = mount(ElProceso)
    const titles = wrapper.findAll('[data-step-title]').map(el => el.text())
    expect(titles).toEqual(['Diseño', 'Confección', 'Entrega'])
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd frontend && npm run test -- ElProceso
```

Expected: FAIL — `ElProceso.vue` not found.

- [ ] **Step 3: Create ElProceso.vue**

Create `frontend/src/features/home/components/ElProceso.vue`:

```vue
<script setup lang="ts">
const steps = [
  {
    number: '01',
    title: 'Diseño',
    body: 'Cada silueta nace de bocetos a mano. Los Angeles define la estructura; México aporta el carácter.',
  },
  {
    number: '02',
    title: 'Confección',
    body: 'Materiales seleccionados pieza por pieza. Costura estructural reforzada. Sin atajos en ninguna etapa.',
  },
  {
    number: '03',
    title: 'Entrega',
    body: 'Empaque minimalista, sin exceso. La prenda llega lista para ser usada. Sin plástico.',
  },
]
</script>

<template>
  <section class="bg-[color:var(--color-obsidian)] py-20 px-[var(--spacing-container)]">
    <div class="max-w-[var(--container-max)] mx-auto">

      <!-- Section header -->
      <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] text-[color:var(--color-amber-accent)]/50 mb-2">
        Vantier
      </p>
      <h2 class="text-[length:var(--text-headline)] font-light uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-ivory)] mb-3">
        El Proceso
      </h2>
      <div class="w-7 h-px bg-[color:var(--color-amber-accent)] mb-12" />

      <!-- Steps grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 divide-y md:divide-y-0 md:divide-x divide-[color:var(--color-amber-accent)]/10">
        <div
          v-for="step in steps"
          :key="step.number"
          class="p-8 md:pl-0 md:pr-8 first:md:pl-0 [&:not(:first-child)]:md:pl-8"
          data-step
        >
          <p
            class="font-mono text-[length:var(--text-micro)] text-[color:var(--color-amber-accent)]/35 tracking-[0.28em] mb-6"
            data-step-number
          >
            {{ step.number }}
          </p>
          <div class="w-5 h-px bg-[color:var(--color-amber-accent)] mb-5" />
          <h3
            class="text-[length:var(--text-small)] font-medium uppercase tracking-[var(--tracking-label)] text-[color:var(--color-ivory)] mb-3"
            data-step-title
          >
            {{ step.title }}
          </h3>
          <p class="text-[length:var(--text-micro)] text-[color:var(--color-ivory)]/35 leading-relaxed">
            {{ step.body }}
          </p>
        </div>
      </div>
    </div>
  </section>
</template>
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd frontend && npm run test -- ElProceso
```

Expected: PASS — 3 tests pass.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/features/home/components/ElProceso.vue \
        frontend/src/features/home/components/__tests__/ElProceso.test.ts
git commit -m "feat(home): ElProceso section — 3-step process, obsidian bg, gold accents"
```

---

### Task 5: NewsletterStrip Component

**Files:**
- Create: `frontend/src/features/home/components/NewsletterStrip.vue`
- Create: `frontend/src/features/home/components/__tests__/NewsletterStrip.test.ts`

- [ ] **Step 1: Write the failing test**

Create `frontend/src/features/home/components/__tests__/NewsletterStrip.test.ts`:

```ts
import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import NewsletterStrip from '../NewsletterStrip.vue'

describe('NewsletterStrip', () => {
  it('renders an anchor tag (not a form)', () => {
    const wrapper = mount(NewsletterStrip)
    expect(wrapper.find('form').exists()).toBe(false)
    expect(wrapper.find('a[data-newsletter-cta]').exists()).toBe(true)
  })

  it('opens in a new tab', () => {
    const wrapper = mount(NewsletterStrip)
    const link = wrapper.find('a[data-newsletter-cta]')
    expect(link.attributes('target')).toBe('_blank')
    expect(link.attributes('rel')).toContain('noopener')
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd frontend && npm run test -- NewsletterStrip
```

Expected: FAIL — `NewsletterStrip.vue` not found.

- [ ] **Step 3: Create NewsletterStrip.vue**

Create `frontend/src/features/home/components/NewsletterStrip.vue`:

```vue
<script setup lang="ts">
// External newsletter signup URL — update when the actual URL is known
const NEWSLETTER_URL = 'https://vantierluxuryla.com/newsletter'
</script>

<template>
  <section class="bg-[color:var(--color-warm-beige-dk)] py-16 px-[var(--spacing-container)] text-center border-y border-[color:var(--color-obsidian)]/6">
    <div class="max-w-[var(--container-max)] mx-auto">

      <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] text-[color:var(--color-obsidian)]/35 mb-3">
        Acceso Exclusivo
      </p>
      <h2 class="text-[length:var(--text-headline)] font-light uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-obsidian)] mb-3">
        Únete al círculo Vantier
      </h2>
      <p class="text-[length:var(--text-small)] text-[color:var(--color-obsidian)]/50 mb-10">
        Suscríbete y recibe 15% de descuento en tu primera compra
      </p>

      <a
        :href="NEWSLETTER_URL"
        target="_blank"
        rel="noopener noreferrer"
        data-newsletter-cta
        class="inline-flex items-center gap-2 border border-[color:var(--color-obsidian)]/20 px-8 py-3.5 text-[length:var(--text-small)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-obsidian)]/60 hover:border-[color:var(--color-obsidian)]/60 hover:text-[color:var(--color-obsidian)] transition-all duration-[var(--duration-normal)]"
      >
        Unirme al círculo
        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </a>
    </div>
  </section>
</template>
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd frontend && npm run test -- NewsletterStrip
```

Expected: PASS — 2 tests pass.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/features/home/components/NewsletterStrip.vue \
        frontend/src/features/home/components/__tests__/NewsletterStrip.test.ts
git commit -m "feat(home): NewsletterStrip — external redirect CTA, no email input"
```

---

### Task 6: AppFooter — Replace Email Form with External Link

**Files:**
- Modify: `frontend/src/shared/components/AppFooter.vue`

- [ ] **Step 1: Remove email form logic from script setup**

In `AppFooter.vue`, remove the `<script setup>` block entirely and replace with:

```vue
<script setup lang="ts">
const NEWSLETTER_URL = 'https://vantierluxuryla.com/newsletter'
</script>
```

- [ ] **Step 2: Replace the newsletter form in the template**

Find the right column (the `<!-- Right: Newsletter + social -->` div) and replace its newsletter sub-section:

```html
<!-- Right: Newsletter + social -->
<div class="flex flex-col gap-6">
  <div>
    <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] opacity-40 mb-4">Stay in the know</p>
    <a
      :href="NEWSLETTER_URL"
      target="_blank"
      rel="noopener noreferrer"
      class="inline-flex items-center gap-2 text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-amber-accent)]/70 hover:text-[color:var(--color-amber-accent)] border-b border-[color:var(--color-amber-accent)]/30 hover:border-[color:var(--color-amber-accent)] pb-px transition-all duration-[var(--duration-fast)]"
    >
      Newsletter — 15% off
      <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </a>
  </div>

  <!-- Social — unchanged -->
  <div class="flex items-center gap-3">
    <a
      href="https://instagram.com/vantierluxuryla"
      target="_blank"
      rel="noopener noreferrer"
      class="opacity-40 hover:opacity-100 transition-opacity duration-[var(--duration-fast)]"
      aria-label="Instagram"
    >
      <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <rect x="2" y="2" width="20" height="20" rx="5" ry="5"/>
        <circle cx="12" cy="12" r="4"/>
        <circle cx="17.5" cy="6.5" r="0.5" fill="currentColor"/>
      </svg>
    </a>
    <span class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-30">@vantierluxuryla</span>
  </div>
</div>
```

Also remove the `<style scoped>` block (the `form-swap` transition is no longer needed).

- [ ] **Step 3: Verify in browser**

Footer should show "Newsletter — 15% off" as a gold link. Clicking opens new tab. No email input visible.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/shared/components/AppFooter.vue
git commit -m "feat(footer): replace newsletter email form with external link CTA"
```

---

### Task 7: HomePage — Wire All Sections in Correct Order

**Files:**
- Modify: `frontend/src/features/home/pages/HomePage.vue`

- [ ] **Step 1: Rewrite HomePage.vue with correct section order**

```vue
<script setup lang="ts">
import HeroCarousel from '../components/HeroCarousel.vue'
import ProductLineGrid from '../components/ProductLineGrid.vue'
import BrandStatement from '../components/BrandStatement.vue'
import FeaturedProducts from '../components/FeaturedProducts.vue'
import ElProceso from '../components/ElProceso.vue'
import NewsletterStrip from '../components/NewsletterStrip.vue'
import SeoHead from '@shared/components/SeoHead.vue'
</script>

<template>
  <SeoHead
    title="Vantier — Silent Luxury Menswear | Los Angeles"
    description="Vantier crafts elevated menswear for the discerning modern man. Polo Atelier jackets, Signature shirts, and Essential tees. Free shipping on 5+ items."
    canonical="https://vantierluxuryla.com/"
  />
  <HeroCarousel />
  <ProductLineGrid />
  <BrandStatement />
  <FeaturedProducts />
  <ElProceso />
  <NewsletterStrip />
</template>
```

Order matches the design spec: Hero → Shop by Line → Brand Statement → Selected Pieces → El Proceso → Newsletter.

- [ ] **Step 2: Verify full homepage scroll in browser**

Open http://localhost:5173. Scroll from top to bottom:
1. Black announcement bar
2. Black sticky nav with gold newsletter link
3. Hero with parallax image
4. ProductLineGrid (3 columns, existing accordion hover)
5. BrandStatement (dark photo left, warm beige text right)
6. FeaturedProducts (warm beige, 3 cards + editorial tile)
7. ElProceso (black, 3 numbered steps)
8. NewsletterStrip (warm beige, single button)
9. Black footer

- [ ] **Step 3: Commit**

```bash
git add frontend/src/features/home/pages/HomePage.vue
git commit -m "feat(home): wire all homepage sections in final design order"
```

---

## Phase 2 — Product Detail Page (PDP)

---

### Task 8: ProductLookbook Component

**Files:**
- Create: `frontend/src/features/products/components/ProductLookbook.vue`

- [ ] **Step 1: Create ProductLookbook.vue**

```vue
<script setup lang="ts">
defineProps<{
  lineName: string
  images?: Array<{ src: string; alt: string }>
}>()
</script>

<template>
  <section class="bg-[color:var(--color-warm-beige)] py-16 px-[var(--spacing-container)]">
    <div class="max-w-[var(--container-max)] mx-auto">

      <!-- Header -->
      <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] text-[color:var(--color-obsidian)]/35 mb-2">
        {{ lineName }}
      </p>
      <h2 class="text-[length:var(--text-headline)] font-light uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-obsidian)] mb-3">
        Lookbook
      </h2>
      <div class="w-7 h-px bg-[color:var(--color-amber-accent)] mb-10" />

      <!-- Photo grid: 3:2 main + 2:3 portrait -->
      <div v-if="images && images.length" class="grid grid-cols-3 gap-2 mb-8">
        <div class="col-span-2 aspect-[4/5] overflow-hidden bg-[color:var(--color-obsidian)]">
          <img
            :src="images[0].src"
            :alt="images[0].alt"
            class="w-full h-full object-cover hover:scale-[1.03] transition-transform duration-[600ms] ease-[var(--ease-luxury)]"
          />
        </div>
        <div v-if="images[1]" class="col-span-1 aspect-[4/5] overflow-hidden bg-[color:var(--color-obsidian)]/20">
          <img
            :src="images[1].src"
            :alt="images[1].alt"
            class="w-full h-full object-cover hover:scale-[1.03] transition-transform duration-[600ms] ease-[var(--ease-luxury)]"
          />
        </div>
      </div>

      <!-- Placeholder when no images provided -->
      <div v-else class="grid grid-cols-3 gap-2 mb-8">
        <div class="col-span-2 aspect-[4/5] bg-[color:var(--color-obsidian)]/10 flex items-center justify-center">
          <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-obsidian)]/25">
            Editorial — Próximamente
          </p>
        </div>
        <div class="col-span-1 aspect-[4/5] bg-[color:var(--color-obsidian)]/6" />
      </div>

      <!-- CTA -->
      <div class="text-center">
        <RouterLink
          to="/shop"
          class="inline-flex items-center gap-2 border border-[color:var(--color-obsidian)]/20 px-8 py-3 text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-obsidian)]/55 hover:border-[color:var(--color-obsidian)]/50 hover:text-[color:var(--color-obsidian)] transition-all duration-[var(--duration-normal)]"
        >
          Ver lookbook completo
          <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </RouterLink>
      </div>
    </div>
  </section>
</template>
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/features/products/components/ProductLookbook.vue
git commit -m "feat(pdp): ProductLookbook — editorial 2-up photo grid with placeholder state"
```

---

### Task 9: CareInstructions Component

**Files:**
- Create: `frontend/src/features/products/components/CareInstructions.vue`
- Create: `frontend/src/features/products/components/__tests__/CareInstructions.test.ts`

- [ ] **Step 1: Write the failing test**

Create `frontend/src/features/products/components/__tests__/CareInstructions.test.ts`:

```ts
import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import CareInstructions from '../CareInstructions.vue'

const CARE_DATA = {
  wash: 'Dry clean solamente',
  iron: 'Temperatura baja, vapor',
  store: 'Colgar, lejos de luz directa',
  material: '100% lana italiana 16 mic',
}

describe('CareInstructions', () => {
  it('renders 4 care items', () => {
    const wrapper = mount(CareInstructions, { props: { care: CARE_DATA, lineName: 'Polo Atelier' } })
    expect(wrapper.findAll('[data-care-item]')).toHaveLength(4)
  })

  it('displays the material', () => {
    const wrapper = mount(CareInstructions, { props: { care: CARE_DATA, lineName: 'Polo Atelier' } })
    expect(wrapper.text()).toContain('100% lana italiana 16 mic')
  })

  it('displays the line name in the header', () => {
    const wrapper = mount(CareInstructions, { props: { care: CARE_DATA, lineName: 'Polo Atelier' } })
    expect(wrapper.text()).toContain('Polo Atelier')
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd frontend && npm run test -- CareInstructions
```

Expected: FAIL — `CareInstructions.vue` not found.

- [ ] **Step 3: Create CareInstructions.vue**

```vue
<script setup lang="ts">
export interface CareData {
  wash: string
  iron: string
  store: string
  material: string
}

defineProps<{
  lineName: string
  care: CareData
}>()

const CARE_ICONS = {
  wash:     { symbol: '≋', label: 'Lavado'     },
  iron:     { symbol: '◻', label: 'Planchado'  },
  store:    { symbol: '∩', label: 'Almacenaje' },
  material: { symbol: '⊞', label: 'Material'   },
} as const
</script>

<template>
  <section class="bg-[color:var(--color-warm-beige-dk)] py-16 px-[var(--spacing-container)] border-t border-[color:var(--color-obsidian)]/6">
    <div class="max-w-[var(--container-max)] mx-auto">

      <!-- Header -->
      <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] text-[color:var(--color-obsidian)]/35 mb-2">
        {{ lineName }}
      </p>
      <h2 class="text-[length:var(--text-headline)] font-light uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-obsidian)] mb-3">
        Cómo cuidar tu prenda
      </h2>
      <div class="w-7 h-px bg-[color:var(--color-amber-accent)] mb-12" />

      <!-- 4 care items -->
      <div class="grid grid-cols-2 md:grid-cols-4 divide-y md:divide-y-0 md:divide-x divide-[color:var(--color-obsidian)]/6">
        <div
          v-for="(icon, key) in CARE_ICONS"
          :key="key"
          class="p-8 text-center"
          data-care-item
        >
          <!-- Square icon border -->
          <div class="w-9 h-9 mx-auto mb-4 border border-[color:var(--color-obsidian)]/15 flex items-center justify-center">
            <span class="text-base text-[color:var(--color-obsidian)]/35">{{ icon.symbol }}</span>
          </div>
          <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-obsidian)]/55 mb-2">
            {{ icon.label }}
          </p>
          <p class="text-[length:var(--text-micro)] text-[color:var(--color-obsidian)]/38 leading-relaxed">
            {{ care[key] }}
          </p>
        </div>
      </div>

      <!-- Closing tagline -->
      <div class="mt-10 pt-8 border-t border-[color:var(--color-obsidian)]/6 flex items-center gap-4">
        <div class="w-5 h-px bg-[color:var(--color-amber-accent)] flex-shrink-0" />
        <p class="text-[length:var(--text-micro)] text-[color:var(--color-obsidian)]/35 leading-relaxed">
          Una prenda bien cuidada dura décadas. Esto no es moda de temporada — es una inversión en tu guardarropa permanente.
        </p>
      </div>
    </div>
  </section>
</template>
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd frontend && npm run test -- CareInstructions
```

Expected: PASS — 3 tests pass.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/features/products/components/CareInstructions.vue \
        frontend/src/features/products/components/__tests__/CareInstructions.test.ts
git commit -m "feat(pdp): CareInstructions — 4-icon care grid with garment-specific data"
```

---

### Task 10: RelatedProducts Component

**Files:**
- Create: `frontend/src/features/products/components/RelatedProducts.vue`
- Create: `frontend/src/features/products/components/__tests__/RelatedProducts.test.ts`

- [ ] **Step 1: Write the failing test**

```ts
import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import RelatedProducts from '../RelatedProducts.vue'
import { createRouter, createMemoryHistory } from 'vue-router'

const router = createRouter({ history: createMemoryHistory(), routes: [{ path: '/:pathMatch(.*)*', component: { template: '<div/>' } }] })

const LINES = [
  { line: 'Signature', href: '/shop?line=signature' },
  { line: 'Essential', href: '/shop?line=essential' },
]

describe('RelatedProducts', () => {
  it('renders the related lines passed as props', async () => {
    const wrapper = mount(RelatedProducts, {
      props: { relatedLines: LINES },
      global: { plugins: [router] },
    })
    await router.isReady()
    expect(wrapper.findAll('[data-related-card]')).toHaveLength(2)
  })

  it('renders a shop-all editorial tile', async () => {
    const wrapper = mount(RelatedProducts, {
      props: { relatedLines: LINES },
      global: { plugins: [router] },
    })
    await router.isReady()
    expect(wrapper.find('[data-shop-all]').exists()).toBe(true)
  })
})
```

Save to `frontend/src/features/products/components/__tests__/RelatedProducts.test.ts`.

- [ ] **Step 2: Run test to verify it fails**

```bash
cd frontend && npm run test -- RelatedProducts
```

Expected: FAIL.

- [ ] **Step 3: Create RelatedProducts.vue**

```vue
<script setup lang="ts">
defineProps<{
  relatedLines: Array<{ line: string; href: string }>
}>()
</script>

<template>
  <section class="bg-[color:var(--color-warm-beige)] py-16 px-[var(--spacing-container)] border-t border-[color:var(--color-obsidian)]/5">
    <div class="max-w-[var(--container-max)] mx-auto">

      <!-- Header -->
      <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] text-[color:var(--color-obsidian)]/35 mb-2">
        De la misma línea
      </p>
      <h2 class="text-[length:var(--text-headline)] font-light uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-obsidian)] mb-3">
        También te puede interesar
      </h2>
      <div class="w-7 h-px bg-[color:var(--color-amber-accent)] mb-10" />

      <!-- Grid: related cards + shop-all tile -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-[var(--spacing-card-gap)]">

        <!-- Related line cards -->
        <RouterLink
          v-for="item in relatedLines"
          :key="item.line"
          :to="item.href"
          class="relative aspect-[3/4] bg-[color:var(--color-obsidian)]/12 overflow-hidden group"
          data-related-card
        >
          <div class="absolute top-0 left-0 w-6 h-px bg-[color:var(--color-amber-accent)]" />
          <div class="absolute bottom-0 left-0 right-0 p-5 bg-gradient-to-t from-[color:var(--color-obsidian)]/20 to-transparent">
            <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-obsidian)]/45 mb-1">
              Line
            </p>
            <h3 class="text-[length:var(--text-small)] font-medium uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-obsidian)]">
              {{ item.line }}
            </h3>
          </div>
          <div
            class="absolute inset-0 border border-[color:var(--color-obsidian)]/0 group-hover:border-[color:var(--color-amber-accent)]/30 transition-colors duration-[var(--duration-normal)]"
          />
        </RouterLink>

        <!-- Shop all editorial tile -->
        <RouterLink
          to="/shop"
          class="relative aspect-[3/4] bg-[color:var(--color-obsidian)] overflow-hidden flex flex-col items-center justify-center group"
          data-shop-all
        >
          <div class="absolute top-0 left-0 w-5 h-px bg-[color:var(--color-amber-accent)]" />
          <div class="text-center px-6">
            <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] text-[color:var(--color-ivory)]/30 mb-2">Ver toda la</p>
            <h3 class="text-[length:var(--text-title)] font-light tracking-[var(--tracking-headline)] text-[color:var(--color-ivory)]/65 group-hover:text-[color:var(--color-ivory)] transition-colors duration-[var(--duration-normal)]">
              Colección →
            </h3>
          </div>
        </RouterLink>
      </div>
    </div>
  </section>
</template>
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd frontend && npm run test -- RelatedProducts
```

Expected: PASS — 2 tests pass.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/features/products/components/RelatedProducts.vue \
        frontend/src/features/products/components/__tests__/RelatedProducts.test.ts
git commit -m "feat(pdp): RelatedProducts — cross-sell cards + shop-all editorial tile"
```

---

### Task 11: Mount PDP Storytelling Sections in ProductDetailPage

**Files:**
- Modify: `frontend/src/features/products/components/ProductDetailPage.vue`

- [ ] **Step 1: Import the three new PDP sections**

In the `<script setup>` block of `ProductDetailPage.vue`, add imports after the existing ones:

```ts
import ProductLookbook from './ProductLookbook.vue'
import CareInstructions from './CareInstructions.vue'
import type { CareData } from './CareInstructions.vue'
import RelatedProducts from './RelatedProducts.vue'
```

- [ ] **Step 2: Add care data and related lines per product line**

In the `<script setup>` block, add after the existing computed/refs:

```ts
const CARE_BY_LINE: Record<string, CareData> = {
  'Polo Atelier': {
    wash:     'Dry clean solamente',
    iron:     'Temperatura baja, vapor',
    store:    'Colgar, lejos de luz directa',
    material: '100% lana italiana 16 mic',
  },
  'Signature': {
    wash:     'Dry clean o lavado a mano',
    iron:     'Temperatura media, sin vapor directo',
    store:    'Colgar en funda de tela',
    material: '95% algodón Pima, 5% elastano',
  },
  'Essential': {
    wash:     'Lavado a máquina, frío',
    iron:     'Temperatura baja',
    store:    'Doblar, no colgar',
    material: '100% algodón Pima 200g',
  },
}

const RELATED_BY_LINE: Record<string, Array<{ line: string; href: string }>> = {
  'Polo Atelier': [
    { line: 'Signature', href: '/shop?line=signature' },
    { line: 'Essential', href: '/shop?line=essential' },
  ],
  'Signature': [
    { line: 'Polo Atelier', href: '/shop?line=polo-atelier' },
    { line: 'Essential',    href: '/shop?line=essential' },
  ],
  'Essential': [
    { line: 'Polo Atelier', href: '/shop?line=polo-atelier' },
    { line: 'Signature',    href: '/shop?line=signature' },
  ],
}

const currentCare = computed(() => CARE_BY_LINE[displayProduct.value.line] ?? CARE_BY_LINE['Polo Atelier'])
const relatedLines = computed(() => RELATED_BY_LINE[displayProduct.value.line] ?? RELATED_BY_LINE['Polo Atelier'])
```

- [ ] **Step 3: Mount sections below the existing PDP content**

At the end of the `<template>`, just before the `<Teleport>` for sticky mobile CTA, add:

```html
  <!-- PDP storytelling sections -->
  <ProductLookbook :line-name="displayProduct.line" />
  <CareInstructions :line-name="displayProduct.line" :care="currentCare" />
  <RelatedProducts :related-lines="relatedLines" />
```

Full bottom of the template should look like:

```html
    </section>

  <!-- PDP storytelling sections -->
  <ProductLookbook :line-name="displayProduct.line" />
  <CareInstructions :line-name="displayProduct.line" :care="currentCare" />
  <RelatedProducts :related-lines="relatedLines" />

  <!-- Sticky Add to Cart — mobile only -->
  <Teleport to="body">
    ...
  </Teleport>

  <!-- Size guide modal -->
  <SizeGuideModal :open="sizeGuideOpen" @close="sizeGuideOpen = false" />
</template>
```

- [ ] **Step 4: Verify PDP scroll in browser**

Navigate to a product page (e.g., http://localhost:5173/shop/mock-1). Scroll down past the product hero:
- Lookbook section appears with warm beige bg and placeholder tiles (or real images if available)
- Care instructions section shows 4 icon squares with correct garment data
- Related products shows 2 other line cards + dark editorial "Colección →" tile

- [ ] **Step 5: Run all tests**

```bash
cd frontend && npm run test
```

Expected: PASS — all tests pass.

- [ ] **Step 6: Commit**

```bash
git add frontend/src/features/products/components/ProductDetailPage.vue
git commit -m "feat(pdp): mount Lookbook, CareInstructions, RelatedProducts below product hero"
```

---

## Phase 3 — Checkout Polish

---

### Task 12: Active Step Indicator → Gold in CheckoutStepper

**Files:**
- Modify: `frontend/src/features/checkout/components/CheckoutStepper.vue`

The stepper already uses obsidian/ivory tokens. The only change: the **active step circle** should use gold (amber accent) instead of obsidian border, to signal "current action" in the luxury palette.

- [ ] **Step 1: Update active step circle to gold**

In `CheckoutStepper.vue`, find the `:class` binding on the circle `<div>` (line 29–35). Change the active branch from obsidian to amber:

```html
<div
  class="w-7 h-7 rounded-full border flex items-center justify-center text-[length:var(--text-micro)] font-semibold transition-colors duration-[var(--duration-normal)]"
  :class="[
    isCompleted(step.key, currentStep)
      ? 'bg-[color:var(--color-obsidian)] border-[color:var(--color-obsidian)] text-[color:var(--color-ivory)]'
      : isActive(step.key, currentStep)
        ? 'border-[color:var(--color-amber-accent)] text-[color:var(--color-amber-accent)]'
        : 'border-[color:var(--color-border)] text-[color:var(--color-border-strong)]'
  ]"
>
```

Also update the step label for the active state to use amber:

```html
<span
  class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] transition-colors duration-[var(--duration-normal)]"
  :class="isActive(step.key, currentStep)
    ? 'text-[color:var(--color-amber-accent)] font-medium'
    : 'text-[color:var(--color-border-strong)]'"
>
  {{ step.label }}
</span>
```

- [ ] **Step 2: Verify in browser**

Navigate to http://localhost:5173/checkout. The current step circle and label should show gold. Completed steps remain obsidian with white checkmark. Inactive steps remain grey.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/features/checkout/components/CheckoutStepper.vue
git commit -m "feat(checkout): gold active step indicator — amber accent for current step"
```

---

## Final Verification

- [ ] **Run full test suite**

```bash
cd frontend && npm run test
```

Expected: All tests pass.

- [ ] **Build check**

```bash
cd frontend && npm run build
```

Expected: No TypeScript errors, no build failures.

- [ ] **Full page review**

Visit and scroll each page:
- `/` — homepage (9 sections, black nav, parallax hero, warm ivory body, black footer)
- `/shop` — catalog (design tokens applied, square corners)
- `/shop/[id]` — PDP (hero split, lookbook, care, related)
- `/checkout` — stepper gold, Playfair titles
