import { describe, it, expect } from 'vitest'
import { isDiscountValid } from '@features/checkout/composables/useCheckout'

describe('isDiscountValid', () => {
  it('allows discount when margin stays above 50%', () => {
    // salePrice=90, margin=(90-40)/90=55.5%
    expect(isDiscountValid({ priceUSD: 100, costUSD: 40, discountAmount: 10 })).toBe(true)
  })

  it('rejects discount when margin drops below 50%', () => {
    // salePrice=70, margin=(70-40)/70=42.8%
    expect(isDiscountValid({ priceUSD: 100, costUSD: 40, discountAmount: 30 })).toBe(false)
  })

  it('allows 0 discount always', () => {
    expect(isDiscountValid({ priceUSD: 100, costUSD: 40, discountAmount: 0 })).toBe(true)
  })

  it('rejects discount when margin equals exactly below 50%', () => {
    // salePrice=99, margin=(99-50)/99=49.5% < 50%
    expect(isDiscountValid({ priceUSD: 100, costUSD: 50, discountAmount: 1 })).toBe(false)
  })
})
