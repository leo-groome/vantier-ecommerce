import { apiClient } from '@shared/api/client'
import type { ShippingRate } from './types'

export async function fetchShippingRates(addressId: string): Promise<ShippingRate[]> {
  const { data } = await apiClient.get<ShippingRate[]>('/shipping/rates', { params: { addressId } })
  return data
}

export async function validateDiscount(code: string): Promise<{ discountAmount: number }> {
  const { data } = await apiClient.post('/discounts/validate', { code })
  return data
}

export async function createOrder(payload: unknown): Promise<{ orderId: string; paymentIntentClientSecret: string }> {
  const { data } = await apiClient.post('/orders', payload)
  return data
}
