import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { CheckoutStep, ShippingRate } from './types'

export const useCheckoutStore = defineStore('checkout', () => {
  const step = ref<CheckoutStep>('address')
  const shippingRate = ref<ShippingRate | null>(null)
  const discountCode = ref<string | null>(null)
  const paymentIntentId = ref<string | null>(null)

  return { step, shippingRate, discountCode, paymentIntentId }
})
