import { apiClient } from '@shared/api/client'
import type { AdminOrder, AdminOrderListResponse, OrderStatus, OrderFilters } from './types'

export async function listAdminOrders(filters: OrderFilters = {}): Promise<AdminOrderListResponse> {
  const params: Record<string, any> = {
    page: filters.page ?? 1,
    page_size: filters.page_size ?? 50,
  }
  if (filters.status && filters.status !== 'all') params.status = filters.status
  if (filters.customer_email) params.customer_email = filters.customer_email
  const { data } = await apiClient.get<AdminOrderListResponse>('/orders', { params })
  return data
}

export async function getAdminOrder(id: string): Promise<AdminOrder> {
  const { data } = await apiClient.get<AdminOrder>(`/orders/${id}`)
  return data
}

export async function updateOrderStatus(id: string, status: OrderStatus): Promise<AdminOrder> {
  const { data } = await apiClient.patch<AdminOrder>(`/orders/${id}/status`, { status })
  return data
}

export async function generateShippingLabel(id: string): Promise<{ label_url: string }> {
  const { data } = await apiClient.post<{ label_url: string }>(`/orders/${id}/shipping-label`)
  return data
}
