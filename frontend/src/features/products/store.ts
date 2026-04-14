import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Product, ProductFilters } from './types'
import { fetchProducts, fetchProduct } from './api'

export const useProductsStore = defineStore('products', () => {
  const catalog = ref<Product[]>([])
  const selected = ref<Product | null>(null)
  const filters = ref<ProductFilters>({})
  const loading = ref(false)

  async function loadCatalog() {
    loading.value = true
    try {
      catalog.value = await fetchProducts(filters.value)
    } catch {
      catalog.value = []
    } finally {
      loading.value = false
    }
  }

  async function loadProduct(id: string) {
    loading.value = true
    try {
      selected.value = await fetchProduct(id)
    } catch {
      selected.value = null
    } finally {
      loading.value = false
    }
  }

  return { catalog, selected, filters, loading, loadCatalog, loadProduct }
})
