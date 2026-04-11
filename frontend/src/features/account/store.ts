import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User, SavedAddress } from './types'

export const useAccountStore = defineStore('account', () => {
  const user = ref<User | null>(null)
  const savedAddresses = ref<SavedAddress[]>([])
  const authToken = ref<string | null>(null)
  return { user, savedAddresses, authToken }
})
