import type { RouteRecordRaw } from 'vue-router'
export const adminOrderRoutes: RouteRecordRaw[] = [
  { path: 'orders', component: () => import('./components/OrdersPage.vue') },
]
