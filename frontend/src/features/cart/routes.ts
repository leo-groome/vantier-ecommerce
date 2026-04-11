import type { RouteRecordRaw } from 'vue-router'

export const cartRoutes: RouteRecordRaw[] = [
  {
    path: '/cart',
    component: () => import('./components/CartPage.vue'),
  },
]
