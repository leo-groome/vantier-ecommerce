import { createRouter, createWebHistory } from 'vue-router'
import { applyRouteGuards } from '@shared/auth/guards'
import StorefrontLayout from '@/pages/StorefrontLayout.vue'
import { productRoutes } from '@features/products/routes'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: StorefrontLayout,
      children: [
        { path: '', redirect: '/products' },
        ...productRoutes,
      ],
    },
  ],
})

router.beforeEach(applyRouteGuards)
export default router
