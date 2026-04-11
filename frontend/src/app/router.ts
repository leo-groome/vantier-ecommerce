import { createRouter, createWebHistory } from 'vue-router'
import { applyRouteGuards } from '@shared/auth/guards'
import StorefrontLayout from '@/pages/StorefrontLayout.vue'
import { productRoutes } from '@features/products/routes'
import { cartRoutes } from '@features/cart/routes'
import { checkoutRoutes } from '@features/checkout/routes'
import { orderRoutes } from '@features/orders/routes'
import { accountRoutes } from '@features/account/routes'
import { exchangeRoutes } from '@features/exchanges/routes'

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
        ...checkoutRoutes,
        ...orderRoutes,
        ...accountRoutes,
        ...exchangeRoutes,
      ],
    },
  ],
})

router.beforeEach(applyRouteGuards)
export default router
