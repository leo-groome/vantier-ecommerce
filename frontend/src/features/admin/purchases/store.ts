import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as api from './api'
import type { PurchaseOrder, POStatus } from './types'

export const useAdminPurchasesStore = defineStore('admin/purchases', () => {
  const orders = ref<PurchaseOrder[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function loadOrders() {
    loading.value = true
    error.value = null
    try {
      orders.value = await api.listPurchaseOrders()
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Error al cargar órdenes de compra'
    } finally {
      loading.value = false
    }
  }

  async function advanceStatus(id: string, status: POStatus): Promise<boolean> {
    try {
      const updated = await api.updatePOStatus(id, status)
      const idx = orders.value.findIndex(o => o.id === id)
      if (idx !== -1) orders.value[idx] = updated
      return true
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Error al actualizar estado'
      return false
    }
  }

  return { orders, loading, error, loadOrders, advanceStatus }
})
