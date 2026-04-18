import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as api from './api'
import type { DiscountCode, DiscountCreatePayload, DiscountUpdatePayload } from './types'

export const useAdminDiscountsStore = defineStore('admin/discounts', () => {
  const discounts = ref<DiscountCode[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function loadDiscounts() {
    loading.value = true
    error.value = null
    try {
      discounts.value = await api.listDiscounts()
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Error al cargar descuentos'
    } finally {
      loading.value = false
    }
  }

  async function addDiscount(payload: DiscountCreatePayload): Promise<DiscountCode | null> {
    try {
      const created = await api.createDiscount(payload)
      discounts.value.unshift(created)
      return created
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Error al crear descuento'
      return null
    }
  }

  async function editDiscount(id: string, payload: DiscountUpdatePayload): Promise<boolean> {
    try {
      const updated = await api.updateDiscount(id, payload)
      const idx = discounts.value.findIndex(d => d.id === id)
      if (idx !== -1) discounts.value[idx] = updated
      return true
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Error al actualizar descuento'
      return false
    }
  }

  return { discounts, loading, error, loadDiscounts, addDiscount, editDiscount }
})
