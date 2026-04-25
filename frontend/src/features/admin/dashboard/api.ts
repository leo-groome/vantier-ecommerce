import { apiClient } from '@shared/api/client'
import { listAdminOrders } from '@features/admin/orders/api'
import type { AdminOrderListResponse } from '@features/admin/orders/types'
import type { LowStockVariant } from '@features/admin/inventory/types'

export interface DashboardData {
  recentOrders: AdminOrderListResponse
  lowStock: LowStockVariant[]
}

export async function fetchDashboardData(): Promise<DashboardData> {
  const [recentOrders, lowStockRes] = await Promise.all([
    listAdminOrders({ page: 1, page_size: 7 }),
    apiClient.get<LowStockVariant[]>('/inventory/low-stock', { params: { threshold: 50 } }),
  ])
  return {
    recentOrders,
    lowStock: lowStockRes.data,
  }
}
