import type { RouteRecordRaw } from 'vue-router'

export const productRoutes: RouteRecordRaw[] = [
  {
    path: '/shop',
    component: () => import('./components/CatalogPage.vue'),
  },
  {
    path: '/shop/:id',
    component: () => import('./components/ProductDetailPage.vue'),
  },
]
