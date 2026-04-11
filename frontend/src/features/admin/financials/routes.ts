import type { RouteRecordRaw } from 'vue-router'
export const financialsRoutes: RouteRecordRaw[] = [
  { path: 'finances', meta: { requireOwner: true }, component: () => import('./components/FinancialsPage.vue') },
]
