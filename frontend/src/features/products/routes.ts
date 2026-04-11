import type { RouteRecordRaw } from 'vue-router'

export const productRoutes: RouteRecordRaw[] = [
  {
    path: '/products',
    component: () => import('./components/ProductsPage.vue'),
  },
  {
    path: '/products/:id',
    component: () => import('./components/ProductsPage.vue'),
  },
]
