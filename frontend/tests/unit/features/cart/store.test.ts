import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useCartStore } from '@features/cart/store'

describe('cart store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('starts empty', () => {
    const cart = useCartStore()
    expect(cart.items).toHaveLength(0)
    expect(cart.totalItems).toBe(0)
  })

  it('freeShipping is false when fewer than 5 items', () => {
    const cart = useCartStore()
    cart.items = [
      { productId: '1', variantId: 'v1', name: 'Polo', size: 'M', color: 'Blanco', priceUSD: 80, quantity: 4 },
    ]
    expect(cart.totalItems).toBe(4)
    expect(cart.freeShipping).toBe(false)
  })

  it('freeShipping is true when 5 or more items', () => {
    const cart = useCartStore()
    cart.items = [
      { productId: '1', variantId: 'v1', name: 'Polo', size: 'M', color: 'Blanco', priceUSD: 80, quantity: 5 },
    ]
    expect(cart.totalItems).toBe(5)
    expect(cart.freeShipping).toBe(true)
  })

  it('subtotal sums price × quantity', () => {
    const cart = useCartStore()
    cart.items = [
      { productId: '1', variantId: 'v1', name: 'Polo', size: 'M', color: 'Blanco', priceUSD: 80, quantity: 2 },
      { productId: '2', variantId: 'v2', name: 'Shirt', size: 'L', color: 'Negro', priceUSD: 100, quantity: 1 },
    ]
    expect(cart.subtotal).toBe(260)
  })
})
