import type { RouteRecordRaw } from 'vue-router'

export const accountRoutes: RouteRecordRaw[] = [
  { path: '/account', component: () => import('./components/AccountPage.vue') },
]
