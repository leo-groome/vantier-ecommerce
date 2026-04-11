import type { RouteRecordRaw } from 'vue-router'
export const dashboardRoutes: RouteRecordRaw[] = [
  { path: 'dashboard', component: () => import('./components/DashboardPage.vue') },
]
