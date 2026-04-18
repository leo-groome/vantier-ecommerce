import { apiClient } from '@shared/api/client'
import type {
  AdminProduct,
  AdminProductListResponse,
  AdminVariant,
  LowStockVariant,
  ProductCreatePayload,
  StockAdjustment,
  StockAdjustmentResponse,
  VariantCreatePayload,
  VariantUpdatePayload,
} from './types'
import type { ProductImage } from '@features/products/types'

// ── Products ────────────────────────────────────────────────────────────────

export async function listAdminProducts(page = 1, pageSize = 50): Promise<AdminProductListResponse> {
  const { data } = await apiClient.get<AdminProductListResponse>('/products', {
    params: { page, page_size: pageSize },
  })
  return data
}

export async function createProduct(payload: ProductCreatePayload): Promise<AdminProduct> {
  const { data } = await apiClient.post<AdminProduct>('/products', payload)
  return data
}

export async function updateProduct(id: string, payload: { name?: string; description?: string; is_active?: boolean }): Promise<AdminProduct> {
  const { data } = await apiClient.patch<AdminProduct>(`/products/${id}`, payload)
  return data
}

export async function deactivateProduct(id: string): Promise<void> {
  await apiClient.delete(`/products/${id}`)
}

// ── Variants ────────────────────────────────────────────────────────────────

export async function addVariant(productId: string, payload: VariantCreatePayload): Promise<AdminVariant> {
  const { data } = await apiClient.post<AdminVariant>(`/products/${productId}/variants`, payload)
  return data
}

export async function updateVariant(productId: string, variantId: string, payload: VariantUpdatePayload): Promise<AdminVariant> {
  const { data } = await apiClient.patch<AdminVariant>(`/products/${productId}/variants/${variantId}`, payload)
  return data
}

export async function deactivateVariant(productId: string, variantId: string): Promise<void> {
  await apiClient.delete(`/products/${productId}/variants/${variantId}`)
}

// ── Stock ───────────────────────────────────────────────────────────────────

export async function adjustStock(variantId: string, payload: StockAdjustment): Promise<StockAdjustmentResponse> {
  const { data } = await apiClient.patch<StockAdjustmentResponse>(`/inventory/variants/${variantId}/stock`, payload)
  return data
}

export async function getLowStockVariants(threshold = 50): Promise<LowStockVariant[]> {
  const { data } = await apiClient.get<LowStockVariant[]>('/inventory/low-stock', {
    params: { threshold },
  })
  return data
}

export function getBarcodeUrl(variantId: string): string {
  return `${apiClient.defaults.baseURL}/inventory/variants/${variantId}/barcode`
}

// ── Images ──────────────────────────────────────────────────────────────────

export async function uploadVariantImage(
  productId: string,
  variantId: string,
  file: File,
  altText?: string,
): Promise<ProductImage> {
  const form = new FormData()
  form.append('file', file)
  if (altText) form.append('alt_text', altText)
  const { data } = await apiClient.post<ProductImage>(
    `/products/${productId}/variants/${variantId}/images/upload`,
    form,
  )
  return data
}

export async function deleteVariantImage(productId: string, variantId: string, imageId: string): Promise<void> {
  await apiClient.delete(`/products/${productId}/variants/${variantId}/images/${imageId}`)
}
