import type { RouteRecordRaw } from 'vue-router'

export const orderRoutes: RouteRecordRaw[] = [
  { path: '/orders', component: () => import('./components/OrdersPage.vue'), meta: { requireAuth: true } },
  { path: '/orders/:id', component: () => import('./components/OrdersPage.vue'), meta: { requireAuth: true } },
]
