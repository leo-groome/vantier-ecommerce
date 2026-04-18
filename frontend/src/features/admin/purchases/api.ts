import { apiClient } from '@shared/api/client'
import type { PurchaseOrder, POCreatePayload, POStatus } from './types'

export async function listPurchaseOrders(): Promise<PurchaseOrder[]> {
  const { data } = await apiClient.get<PurchaseOrder[]>('/purchase-orders')
  return data
}

export async function getPurchaseOrder(id: string): Promise<PurchaseOrder> {
  const { data } = await apiClient.get<PurchaseOrder>(`/purchase-orders/${id}`)
  return data
}

export async function createPurchaseOrder(payload: POCreatePayload): Promise<PurchaseOrder> {
  const { data } = await apiClient.post<PurchaseOrder>('/purchase-orders', payload)
  return data
}

export async function updatePOStatus(id: string, status: POStatus): Promise<PurchaseOrder> {
  const { data } = await apiClient.patch<PurchaseOrder>(`/purchase-orders/${id}/status`, { status })
  return data
}
