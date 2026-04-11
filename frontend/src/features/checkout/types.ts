export type CheckoutStep = 'address' | 'shipping' | 'payment' | 'confirmation'

export interface ShippingRate {
  carrierId: string
  carrierName: string
  service: string
  priceUSD: number
  estimatedDays: number
}

export interface DiscountValidationInput {
  priceUSD: number
  costUSD: number
  discountAmount: number
}
