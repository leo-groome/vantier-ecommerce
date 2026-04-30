import type { RouteRecordRaw } from 'vue-router'
export const homepageConfigRoutes: RouteRecordRaw[] = [
  { path: 'homepage', component: () => import('./components/HomepageAdminPage.vue') },
]
