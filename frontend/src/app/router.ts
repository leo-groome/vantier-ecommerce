import { createRouter, createWebHistory } from 'vue-router'
import { applyRouteGuards } from '@shared/auth/guards'
import StorefrontLayout from '@/pages/StorefrontLayout.vue'
import { productRoutes } from '@features/products/routes'
import { cartRoutes } from '@features/cart/routes'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: StorefrontLayout,
      children: [
        { path: '', redirect: '/products' },
        ...productRoutes,
        ...cartRoutes,
      ],
    },
  ],
})

router.beforeEach(applyRouteGuards)
export default router
