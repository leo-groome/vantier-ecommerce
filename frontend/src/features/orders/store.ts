import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Order } from './types'

export const useOrdersStore = defineStore('orders', () => {
  const orders = ref<Order[]>([])
  const selected = ref<Order | null>(null)
  return { orders, selected }
})
