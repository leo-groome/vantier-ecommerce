import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as api from './api'
import type { AdminOrder, OrderStatus, OrderFilters } from './types'

export const useAdminOrdersStore = defineStore('admin/orders', () => {
  const orders = ref<AdminOrder[]>([])
  const total = ref(0)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function loadOrders(filters: OrderFilters = {}) {
    loading.value = true
    error.value = null
    try {
      const res = await api.listAdminOrders(filters)
      orders.value = res.items
      total.value = res.total
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Error al cargar órdenes'
    } finally {
      loading.value = false
    }
  }

  async function changeStatus(orderId: string, status: OrderStatus): Promise<boolean> {
    try {
      const updated = await api.updateOrderStatus(orderId, status)
      const idx = orders.value.findIndex(o => o.id === orderId)
      if (idx !== -1) orders.value[idx] = updated
      return true
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Error al actualizar estado'
      return false
    }
  }

  async function requestShippingLabel(orderId: string): Promise<string | null> {
    try {
      const res = await api.generateShippingLabel(orderId)
      return res.label_url
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Error al generar etiqueta'
      return null
    }
  }

  return { orders, total, loading, error, loadOrders, changeStatus, requestShippingLabel }
})
