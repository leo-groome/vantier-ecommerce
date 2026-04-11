import { createRouter, createWebHistory } from 'vue-router'
import { applyRouteGuards } from '@shared/auth/guards'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/products' },
  ],
})

router.beforeEach(applyRouteGuards)

export default router
