import type { RouteRecordRaw } from 'vue-router'
import AdminLayout from '@/pages/AdminLayout.vue'
import { dashboardRoutes } from './dashboard/routes'
import { inventoryRoutes } from './inventory/routes'
import { adminOrderRoutes } from './orders/routes'
import { purchaseRoutes } from './purchases/routes'
import { discountRoutes } from './discounts/routes'
import { financialsRoutes } from './financials/routes'
import { userRoutes } from './users/routes'
import { homepageConfigRoutes } from './homepage/routes'

export const adminRoutes: RouteRecordRaw[] = [
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requireAdmin: true },
    children: [
      { path: '', redirect: '/admin/dashboard' },
      ...dashboardRoutes,
      ...inventoryRoutes,
      ...adminOrderRoutes,
      ...purchaseRoutes,
      ...discountRoutes,
      ...financialsRoutes,
      ...userRoutes,
      ...homepageConfigRoutes,
    ],
  },
]
