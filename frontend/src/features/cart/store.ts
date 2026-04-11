import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { CartItem } from './types'

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([])

  const totalItems = computed(() =>
    items.value.reduce((sum, item) => sum + item.quantity, 0)
  )

  const subtotal = computed(() =>
    items.value.reduce((sum, item) => sum + item.priceUSD * item.quantity, 0)
  )

  const freeShipping = computed(() => totalItems.value >= 5)

  function addItem(item: CartItem) {
    const existing = items.value.find((i) => i.variantId === item.variantId)
    if (existing) {
      existing.quantity += item.quantity
    } else {
      items.value.push(item)
    }
  }

  function removeItem(variantId: string) {
    items.value = items.value.filter((i) => i.variantId !== variantId)
  }

  function clear() {
    items.value = []
  }

  return { items, totalItems, subtotal, freeShipping, addItem, removeItem, clear }
})
