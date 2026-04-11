import type { RouteRecordRaw } from 'vue-router'

export const checkoutRoutes: RouteRecordRaw[] = [
  {
    path: '/checkout',
    component: () => import('./components/CheckoutPage.vue'),
    meta: { requireAuth: true, requireCart: true },
  },
]
