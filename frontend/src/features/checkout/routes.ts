import type { RouteRecordRaw } from 'vue-router'

export const checkoutRoutes: RouteRecordRaw[] = [
  {
    path: '/checkout',
    component: () => import('./components/CheckoutPage.vue'),
    meta: { requireCart: true },
  },
  {
    path: '/checkout/success',
    component: () => import('./components/CheckoutSuccessPage.vue'),
    meta: { robots: 'noindex' },
  },
  {
    path: '/checkout/cancel',
    component: () => import('./components/CheckoutCancelPage.vue'),
    meta: { robots: 'noindex' },
  },
  {
    path: '/order-confirm/:orderId',
    component: () => import('./components/OrderConfirmPage.vue'),
    meta: { robots: 'noindex' },
  },
]
