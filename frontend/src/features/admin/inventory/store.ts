import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as api from './api'
import type { AdminProduct, ProductCreatePayload, VariantCreatePayload } from './types'

export const useAdminInventoryStore = defineStore('admin/inventory', () => {
  const products = ref<AdminProduct[]>([])
  const total = ref(0)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function loadProducts() {
    loading.value = true
    error.value = null
    try {
      const res = await api.listAdminProducts()
      products.value = res.items
      total.value = res.total
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Failed to load products'
    } finally {
      loading.value = false
    }
  }

  async function createProduct(payload: ProductCreatePayload): Promise<AdminProduct | null> {
    try {
      const product = await api.createProduct(payload)
      products.value.unshift(product)
      total.value++
      return product
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Failed to create product'
      return null
    }
  }

  async function addVariant(productId: string, payload: VariantCreatePayload): Promise<boolean> {
    try {
      const variant = await api.addVariant(productId, payload)
      const product = products.value.find(p => p.id === productId)
      if (product) product.variants.push(variant)
      return true
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Failed to add variant'
      return false
    }
  }

  async function adjustStock(variantId: string, delta: number, reason?: string): Promise<boolean> {
    try {
      const res = await api.adjustStock(variantId, { delta, reason })
      // Update stock in place
      for (const product of products.value) {
        const variant = product.variants.find(v => v.id === variantId)
        if (variant) {
          variant.stock_qty = res.new_qty
          break
        }
      }
      return true
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Failed to adjust stock'
      return false
    }
  }

  async function deactivateProduct(productId: string): Promise<boolean> {
    try {
      await api.deactivateProduct(productId)
      const idx = products.value.findIndex(p => p.id === productId)
      if (idx !== -1) products.value[idx].is_active = false
      return true
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Failed to deactivate product'
      return false
    }
  }

  return {
    products,
    total,
    loading,
    error,
    loadProducts,
    createProduct,
    addVariant,
    adjustStock,
    deactivateProduct,
  }
})
