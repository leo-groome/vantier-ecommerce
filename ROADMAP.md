# Vantier MVP — Roadmap de Lanzamiento

> Actualizar este archivo al completar cada tarea. Leyenda: ✅ Hecho · 🔄 En progreso · ⬜ Pendiente · 🚫 Bloqueado

---

## Dominios (referencia)
| Subdominio | Propósito | Estado |
|------------|-----------|--------|
| `vantierluxuryla.com` | Landing page | ✅ Live |
| `shop.vantierluxuryla.com` | E-commerce | ⬜ Pendiente deploy |
| `assets.vantierluxuryla.com` | CDN imágenes | 🚫 Bloqueado — DNS en GoDaddy, requiere credenciales del cliente |

---

## Phase 0 — Configuración de ENV ✅ Completa

### Backend `backend/.env`
| Variable | Estado | Notas |
|----------|--------|-------|
| `DATABASE_URL` | ✅ | Neon DB configurado |
| `NEON_AUTH_JWKS_URL` | ✅ | Configurado |
| `NEON_AUTH_AUDIENCE` | ✅ | Configurado |
| `STRIPE_SECRET_KEY` | ✅ | `rk_test_...` (restricted key) |
| `STRIPE_WEBHOOK_SECRET` | ✅ | `whsec_...` configurado |
| `ENVIA_API_KEY` | ✅ | Clave real configurada |
| `RESEND_API_KEY` | ✅ | Configurado |
| `CLOUDFLARE_ACCOUNT_ID` | ✅ | R2 configurado |
| `R2_BUCKET` / `R2_ACCESS_KEY_ID` / `R2_SECRET_ACCESS_KEY` | ✅ | R2 configurado |
| `R2_PUBLIC_URL` | ✅ | `pub-xxx.r2.dev` |

### Frontend `frontend/.env`
| Variable | Estado | Notas |
|----------|--------|-------|
| `VITE_API_URL` | ✅ | `http://localhost:8000` (sin `/api/v1` — el client lo agrega) |
| `VITE_NEON_AUTH_URL` | ✅ | Configurado |
| `VITE_STRIPE_PUBLISHABLE_KEY` | ✅ | `pk_test_51TMwxj...` configurado |

### Para producción (Railway + Vercel) — aún pendiente
| Variable | Notas |
|----------|-------|
| `ENVIRONMENT=production` | Cambiar en Railway |
| `FRONTEND_URL=https://shop.vantierluxuryla.com` | Cambiar en Railway |
| `CORS_ORIGINS=["https://shop.vantierluxuryla.com"]` | Cambiar en Railway |
| `VITE_API_URL=https://<backend>.railway.app` | Cambiar en Vercel |

---

## Phase 1 — Imágenes (R2 directo para MVP)
> Cloudflare Images requiere plan de pago ($5/mes) — descartado para MVP.
> R2 con URL pública `*.r2.dev` funciona en producción sin configuración extra.
> Post-MVP: migrar DNS → agregar custom domain en R2 → habilitar transformaciones vía `/cdn-cgi/image/`.

| # | Tarea | Estado |
|---|-------|--------|
| 1.1 | `cloudflare_client.py` usa R2/S3 — URLs `*.r2.dev` públicas | ✅ |
| 1.2 | `config.py` usa variables R2 (`cloudflare_account_id`, `r2_bucket`, etc.) | ✅ |
| 1.3 | Verificar que frontend muestra URLs de R2 en PDP y admin | ⬜ Manual |
| 1.4 | Test: subir imagen desde admin → URL `r2.dev` carga en PDP | ⬜ Manual |

---

## Phase 2 — Envia.com (Tarifas de envío reales) ✅ Código completo

| # | Tarea | Estado |
|---|-------|--------|
| 2.1 | `get_shipping_rates()` retorna `list[dict]` con todos los carriers | ✅ |
| 2.2 | Stub fallback retorna 2 opciones mock cuando API key no configurada | ✅ |
| 2.3 | `GET /api/v1/shipping/rates?zip=&item_count=` implementado | ✅ |
| 2.4 | Shipping router registrado en `main.py` | ✅ |
| 2.5 | `OrderCreate` recibe `shipping_usd` y `selected_carrier_name` | ✅ |
| 2.6 | `create_order()` usa `data.shipping_usd` del frontend | ✅ |
| 2.7 | `fetchShippingRates(zip, itemCount)` llama `/api/v1/shipping/rates` | ✅ |
| 2.8 | `ShippingMethodSelect.vue` wired al API real | ✅ |
| 2.9 | Rate seleccionada pasa al checkout store y al payload de la orden | ✅ |
| 2.10 | ✅ Verificado en browser — envia.com retorna tarifas reales | ✅ |

---

## Phase 3 — Stripe Payment Element (pago embebido) 🔄 En pruebas

### Backend ✅ Completo
| # | Tarea | Estado |
|---|-------|--------|
| 3.1 | `create_payment_intent()` en `stripe_client.py` | ✅ |
| 3.2 | Schema `PaymentIntentResponse(order_id, client_secret, amount_cents)` | ✅ |
| 3.3 | `create_order_with_payment_intent()` en service | ✅ |
| 3.4 | `POST /api/v1/orders/create-payment-intent` | ✅ |
| 3.5 | Webhook maneja `payment_intent.succeeded` | ✅ |
| 3.6 | `_finalize_paid_order()` compartido entre Checkout Session y PaymentIntent | ✅ |
| 3.7 | `GET /orders/confirmation/{order_id}` público (solo órdenes pagadas) | ✅ |

### Frontend 🔄 En pruebas
| # | Tarea | Estado |
|---|-------|--------|
| 3.8 | `createPaymentIntent(payload)` en `api.ts` | ✅ |
| 3.9 | `clientSecret` y `orderId` en checkout store | ✅ |
| 3.10 | PaymentIntent se crea al continuar desde shipping | ✅ |
| 3.11 | `StripePaymentForm.vue` monta Payment Element in-page | ✅ |
| 3.12 | `stripe.confirmPayment()` con errores inline, sin redirect externo | ✅ |
| 3.13 | `VITE_STRIPE_PUBLISHABLE_KEY` configurada con clave real | ✅ |
| 3.14 | Test E2E: tarjeta `4242 4242 4242 4242` → pago sin salir del sitio | ⬜ Pendiente |
| 3.15 | Test webhook: `payment_intent.succeeded` → order `status=paid` | ⬜ Pendiente |

> **Nota:** backend usa `rk_test_` (restricted key). Si hay errores de permisos, cambiar a `sk_test_` estándar.

---

## Phase 4 — Pantalla de Confirmación de Pedido ✅ Código completo

| # | Tarea | Estado |
|---|-------|--------|
| 4.1 | `GET /orders/confirmation/{order_id}` — solo retorna órdenes pagadas | ✅ |
| 4.2 | `get_order_confirmation()` en service | ✅ |
| 4.3 | `CheckoutSuccessPage.vue` lee `order_id` de query params | ✅ |
| 4.4 | Fetch con retry (5× / 1.5s) — muestra items, totales, dirección, tracking | ✅ |
| 4.5 | Cart + checkout store se limpian en `onMounted()` | ✅ |
| 4.6 | Test: post-pago → confirmación muestra detalle completo | ⬜ Pendiente |

---

## Verificación Final E2E

| # | Escenario | Estado |
|---|-----------|--------|
| E1 | Subir imagen admin → carga en PDP vía URL `r2.dev` | ⬜ |
| E2 | Checkout completo: dirección → tarifas envia → pago embebido → confirmación | ⬜ |
| E3 | Email confirmación llega al cliente post-pago | ⬜ |
| E4 | Email alerta nuevo pedido llega al admin | ⬜ |
| E5 | Stock decrementa correctamente al confirmar pago | ⬜ |
| E6 | Código de descuento aplica en checkout | ⬜ |
| E7 | Admin genera etiqueta de envío desde panel de órdenes | ⬜ |

---

## Post-MVP

| Tarea | Prioridad |
|-------|-----------|
| Deploy: backend en Railway + frontend en Vercel con env vars de producción | 🔴 Alta |
| Migrar DNS GoDaddy → Cloudflare → activar `shop.vantierluxuryla.com` | 🔴 Alta |
| Custom domain en R2 → habilitar transformaciones de imagen | 🟡 Media |
| Financials dashboard backend (`/api/v1/financials`) | 🟡 Media |
| Order history page — wire `GET /orders/my` en frontend | 🟡 Media |
| Exchanges API wiring en frontend | 🟡 Media |
| E2E tests con Playwright (flujo crítico checkout) | 🟡 Media |
| CSV bulk import/export de inventario | 🟢 Baja |
| Cambiar `rk_test_` → `sk_live_` en producción | 🔴 Antes de go-live |

---

*Última actualización: 2026-04-22 — ENV 100% configurado. Phases 1–4 implementadas. Bloqueador actual: test E2E del Payment Element con `pk_test_` real.*
