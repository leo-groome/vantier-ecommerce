import { createRouter, createWebHistory } from 'vue-router'
import { applyRouteGuards } from '@shared/auth/guards'
import StorefrontLayout from '@/pages/StorefrontLayout.vue'
import AuthLayout from '@/pages/AuthLayout.vue'
import { productRoutes } from '@features/products/routes'
import { cartRoutes } from '@features/cart/routes'
import { checkoutRoutes } from '@features/checkout/routes'
import { orderRoutes } from '@features/orders/routes'
import { accountRoutes } from '@features/account/routes'
import { exchangeRoutes } from '@features/exchanges/routes'
import { adminRoutes } from '@features/admin/routes'

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
    ...adminRoutes,
    {
      path: '/auth',
      component: AuthLayout,
      children: [
        { path: 'login', component: () => import('@features/auth/components/LoginPage.vue') },
      ],
    },
  ],
})

router.beforeEach(applyRouteGuards)
export default router
