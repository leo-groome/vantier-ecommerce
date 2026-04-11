import type { DiscountValidationInput } from '../types'

const MINIMUM_MARGIN = 0.5

export function isDiscountValid({
  priceUSD,
  costUSD,
  discountAmount,
}: DiscountValidationInput): boolean {
  const salePrice = priceUSD - discountAmount
  if (salePrice <= 0) return false
  const margin = (salePrice - costUSD) / salePrice
  return margin >= MINIMUM_MARGIN
}
