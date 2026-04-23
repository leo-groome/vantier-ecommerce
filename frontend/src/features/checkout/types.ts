export type CheckoutStep = 'address' | 'shipping' | 'payment' | 'confirmation'

export interface ShippingRate {
  carrier_id: string
  carrier_name: string
  service: string
  price_usd: number
  estimated_days: number
}

export interface DiscountValidationInput {
  priceUSD: number
  costUSD: number
  discountAmount: number
}
