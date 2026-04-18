import { apiClient } from '@shared/api/client'
import type { DiscountCode, DiscountCreatePayload, DiscountUpdatePayload } from './types'

export async function listDiscounts(): Promise<DiscountCode[]> {
  const { data } = await apiClient.get<DiscountCode[]>('/discounts')
  return data
}

export async function getDiscount(id: string): Promise<DiscountCode> {
  const { data } = await apiClient.get<DiscountCode>(`/discounts/${id}`)
  return data
}

export async function createDiscount(payload: DiscountCreatePayload): Promise<DiscountCode> {
  const { data } = await apiClient.post<DiscountCode>('/discounts', payload)
  return data
}

export async function updateDiscount(id: string, payload: DiscountUpdatePayload): Promise<DiscountCode> {
  const { data } = await apiClient.patch<DiscountCode>(`/discounts/${id}`, payload)
  return data
}
