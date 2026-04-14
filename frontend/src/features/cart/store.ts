import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import type { CartItem } from './types'

const STORAGE_KEY = 'vantier_cart'

function loadFromStorage(): CartItem[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>(loadFromStorage())

  const totalItems = computed(() =>
    items.value.reduce((sum, item) => sum + item.quantity, 0)
  )

  const subtotal = computed(() =>
    items.value.reduce((sum, item) => sum + item.priceUSD * item.quantity, 0)
  )

  const freeShipping = computed(() => totalItems.value >= 5)

  // Persist to localStorage on every change
  watch(items, (val) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(val))
  }, { deep: true })

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
    localStorage.removeItem(STORAGE_KEY)
  }

  return { items, totalItems, subtotal, freeShipping, addItem, removeItem, clear }
})
