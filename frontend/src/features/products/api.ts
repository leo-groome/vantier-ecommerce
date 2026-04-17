import { apiClient } from '@shared/api/client'
import type { Product, ProductFilters, ProductListResponse } from './types'

export async function fetchProducts(filters?: ProductFilters): Promise<Product[]> {
  const { data } = await apiClient.get<ProductListResponse>('/products', { params: filters })
  return data.items
}

export async function fetchProduct(id: string): Promise<Product> {
  const { data } = await apiClient.get<Product>(`/products/${id}`)
  return data
}
