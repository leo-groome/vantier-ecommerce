import { apiClient } from '@shared/api/client'
import type { Product, ProductFilters } from './types'
import { MOCK_PRODUCTS } from './mockData'

function applyFilters(products: Product[], filters?: ProductFilters): Product[] {
  let list = products
  if (filters?.line)  list = list.filter(p => p.line === filters.line)
  if (filters?.style) list = list.filter(p => p.style === filters.style)
  if (filters?.size)  list = list.filter(p => p.variants.some(v => v.size === filters.size))
  if (filters?.color) list = list.filter(p => p.variants.some(v => v.color === filters.color))
  return list
}

export async function fetchProducts(filters?: ProductFilters): Promise<Product[]> {
  try {
    const { data } = await apiClient.get<Product[]>('/products', { params: filters })
    if (Array.isArray(data) && data.length > 0) return data
    return applyFilters(MOCK_PRODUCTS, filters)
  } catch {
    return applyFilters(MOCK_PRODUCTS, filters)
  }
}

export async function fetchProduct(id: string): Promise<Product | null> {
  try {
    const { data } = await apiClient.get<Product>(`/products/${id}`)
    return data
  } catch {
    return MOCK_PRODUCTS.find(p => p.id === id) ?? null
  }
}
