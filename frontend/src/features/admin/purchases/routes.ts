import type { RouteRecordRaw } from 'vue-router'
export const purchaseRoutes: RouteRecordRaw[] = [
  { path: 'purchases', component: () => import('./components/PurchasesPage.vue') },
]
