import type { RouteRecordRaw } from 'vue-router'

export const checkoutRoutes: RouteRecordRaw[] = [
  {
    path: '/checkout',
    component: () => import('./components/CheckoutPage.vue'),
    meta: { requireCart: true },
  },
  {
    path: '/order-confirm/:orderId',
    component: () => import('./components/OrderConfirmPage.vue'),
    meta: { robots: 'noindex' },
  },
]
