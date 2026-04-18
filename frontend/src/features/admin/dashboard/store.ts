import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as api from './api'
import type { AdminOrder } from '@features/admin/orders/types'
import type { LowStockVariant } from '@features/admin/inventory/types'

export const useAdminDashboardStore = defineStore('admin/dashboard', () => {
  const recentOrders = ref<AdminOrder[]>([])
  const totalOrders = ref(0)
  const lowStock = ref<LowStockVariant[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const lowStockCount = computed(() => lowStock.value.length)

  async function loadDashboard() {
    loading.value = true
    error.value = null
    try {
      const data = await api.fetchDashboardData()
      recentOrders.value = data.recentOrders.items
      totalOrders.value = data.recentOrders.total
      lowStock.value = data.lowStock
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Error al cargar dashboard'
    } finally {
      loading.value = false
    }
  }

  return { recentOrders, totalOrders, lowStock, lowStockCount, loading, error, loadDashboard }
})
