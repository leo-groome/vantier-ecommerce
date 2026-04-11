import type { RouteRecordRaw } from 'vue-router'
export const userRoutes: RouteRecordRaw[] = [
  { path: 'users', meta: { requireOwner: true }, component: () => import('./components/UsersPage.vue') },
]
