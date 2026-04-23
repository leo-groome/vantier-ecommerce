import { apiClient } from '@shared/api/client'
import type { ShippingRate } from './types'

export interface OrderItemPayload {
  variant_id: string
  qty: number
}

export interface ShippingAddressPayload {
  full_name: string
  line1: string
  line2?: string
  city: string
  state: string
  zip: string
  country: string
  phone?: string
}

export interface OrderCreatePayload {
  customer_email: string
  customer_name: string
  items: OrderItemPayload[]
  shipping_address: ShippingAddressPayload
  discount_code?: string | null
  selected_carrier_name: string
  shipping_usd: number
}

export interface CheckoutResponse {
  order_id: string
  checkout_url: string
}

export interface PaymentIntentResponse {
  order_id: string
  client_secret: string
  amount_cents: number
}

export async function fetchShippingRates(zip: string, item_count: number): Promise<ShippingRate[]> {
  const { data } = await apiClient.get<ShippingRate[]>('/shipping/rates', { params: { zip, item_count } })
  return data
}

export async function createPaymentIntent(payload: OrderCreatePayload): Promise<PaymentIntentResponse> {
  const { data } = await apiClient.post<PaymentIntentResponse>('/orders/create-payment-intent', payload)
  return data
}

export async function validateDiscount(code: string): Promise<{ discountAmount: number }> {
  const { data } = await apiClient.post('/discounts/validate', { code })
  return data
}

export async function createOrder(payload: OrderCreatePayload): Promise<CheckoutResponse> {
  const { data } = await apiClient.post<CheckoutResponse>('/orders/checkout', payload)
  return data
}
