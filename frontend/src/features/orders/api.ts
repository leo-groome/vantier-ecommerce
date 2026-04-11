import { apiClient } from '@shared/api/client'
import type { Order } from './types'

export async function fetchOrders(): Promise<Order[]> {
  const { data } = await apiClient.get<Order[]>('/orders')
  return data
}

export async function fetchOrder(id: string): Promise<Order> {
  const { data } = await apiClient.get<Order>(`/orders/${id}`)
  return data
}
