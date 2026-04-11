import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Exchange } from './types'

export const useExchangesStore = defineStore('exchanges', () => {
  const exchanges = ref<Exchange[]>([])
  return { exchanges }
})
