# Frontend VSA Architecture Design

**Date:** 2026-04-10  
**Project:** Vantier E-Commerce  
**Status:** Implemented

## Overview

Single Vite SPA using Vertical Slice Architecture + Shared Layer for the Vantier luxury men's clothing platform. Serves two audiences: public storefront (customers) and internal admin panel (Owner/Operative roles).

## Tech Stack

| Tool | Version |
|---|---|
| Framework | Vue 3 |
| Build | Vite 8 |
| Language | TypeScript |
| Styling | Tailwind CSS v4 |
| Components | shadcn-vue |
| State | Pinia |
| Routing | Vue Router 4 |
| Auth | Neon Auth SDK |
| i18n | vue-i18n 9 |
| Testing | Vitest + Playwright |

## Architecture: VSA + Shared Layer

Feature slices own their domain logic. Shared layer provides cross-cutting infrastructure. Rule: slices import from `shared/`, never from each other.

### Directory Structure

```
src/
├── app/              # Bootstrapping (router, plugins, App.vue, main.ts)
├── features/         # Domain slices
│   ├── products/
│   ├── cart/
│   ├── checkout/
│   ├── orders/
│   ├── account/
│   ├── exchanges/
│   └── admin/
│       ├── dashboard/
│       ├── inventory/
│       ├── orders/
│       ├── purchases/
│       ├── discounts/
│       ├── financials/
│       └── users/
├── shared/
│   ├── api/          # HTTP client + JWT interceptor
│   ├── auth/         # Route guards
│   ├── i18n/         # vue-i18n config + lazy loader
│   └── utils/        # formatters (USD, date, size)
└── pages/            # Layouts (Storefront, Admin, Auth)
```

### Slice Anatomy

Every slice follows this structure:
```
features/<slice>/
├── components/   # Vue SFCs
├── composables/  # Business logic
├── store.ts      # Pinia store
├── api.ts        # Backend calls
├── types.ts      # TypeScript interfaces
├── routes.ts     # Route definitions + meta
└── i18n/{ es.json, en.json }
```

## Routing Strategy

Routes declared per slice, assembled in `app/router.ts`.

| Layout | Routes |
|---|---|
| StorefrontLayout | /, /products, /products/:id, /cart, /checkout, /orders, /account, /exchanges |
| AdminLayout | /admin/dashboard, /admin/inventory, /admin/orders, /admin/purchases, /admin/discounts, /admin/finances, /admin/users |
| AuthLayout | /auth/login |

### Route Guards (shared/auth/guards.ts)

| Guard | Routes | Condition |
|---|---|---|
| requireAuth | /account, /checkout, /orders, /exchanges | Valid Neon Auth session |
| requireAdmin | /admin/* | Role: Owner or Operative |
| requireOwner | /admin/finances, /admin/users | Role: Owner only |
| requireCart | /checkout | Cart not empty |

## State Management

One Pinia store per slice. No global monolithic store.

| Slice | Key state |
|---|---|
| products | catalog, selected, filters, loading |
| cart | items, totalItems, subtotal, freeShipping (≥5 items) |
| checkout | step, shippingRate, discountCode, paymentIntentId |
| account | user, savedAddresses, authToken |

## Business Rules Encoded in Frontend

1. **Free shipping** — `freeShipping = totalItems >= 5` in cart store
2. **Margin floor** — `isDiscountValid()` in checkout composable; rejects discounts where `(salePrice - cost) / salePrice < 0.5`

## i18n

Languages: ES (default), EN. Each slice owns `i18n/es.json` and `i18n/en.json`. `shared/i18n/index.ts` loads them lazily via `loadSliceMessages(slice, locale)`.

## Testing

| Type | Tool | Coverage |
|---|---|---|
| Unit | Vitest | formatters, cart store (free shipping), checkout composable (margin validation) |
| E2E | Playwright | storefront navigation, auth guard redirects |

## Vite Aliases

| Alias | Path |
|---|---|
| `@` | `src/` |
| `@features` | `src/features/` |
| `@shared` | `src/shared/` |
