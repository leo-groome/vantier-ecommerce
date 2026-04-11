import type { RouteRecordRaw } from 'vue-router'
export const discountRoutes: RouteRecordRaw[] = [
  { path: 'discounts', component: () => import('./components/DiscountsPage.vue') },
]
