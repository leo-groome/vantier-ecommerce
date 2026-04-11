import type { RouteRecordRaw } from 'vue-router'
export const inventoryRoutes: RouteRecordRaw[] = [
  { path: 'inventory', component: () => import('./components/InventoryPage.vue') },
]
