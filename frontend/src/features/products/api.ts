import { apiClient } from '@shared/api/client'
import type { Product, ProductFilters } from './types'

export async function fetchProducts(filters?: ProductFilters): Promise<Product[]> {
  const { data } = await apiClient.get<Product[]>('/products', { params: filters })
  return data
}

export async function fetchProduct(id: string): Promise<Product> {
  const { data } = await apiClient.get<Product>(`/products/${id}`)
  return data
}
