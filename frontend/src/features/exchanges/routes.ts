import type { RouteRecordRaw } from 'vue-router'

export const exchangeRoutes: RouteRecordRaw[] = [
  { path: '/exchanges', component: () => import('./components/ExchangesPage.vue'), meta: { requireAuth: true } },
]
