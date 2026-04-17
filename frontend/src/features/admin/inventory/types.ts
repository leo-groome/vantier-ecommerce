import type { ProductLine, ProductStyle, ProductSize, ProductImage } from '@features/products/types'

export type { ProductLine, ProductStyle, ProductSize }

export interface AdminVariant {
  id: string
  sku: string
  style: ProductStyle
  size: ProductSize
  color: string
  stock_qty: number
  price_usd: string
  cost_acquisition_usd: string
  is_active: boolean
  images: ProductImage[]
}

export interface AdminProduct {
  id: string
  name: string
  line: ProductLine
  description: string | null
  is_active: boolean
  variants: AdminVariant[]
}

export interface AdminProductListResponse {
  items: AdminProduct[]
  total: number
  page: number
  page_size: number
}

export interface ProductCreatePayload {
  line: ProductLine
  name: string
  description?: string
}

export interface VariantCreatePayload {
  style: ProductStyle
  size: ProductSize
  color: string
  price_usd: number
  cost_acquisition_usd: number
  stock_qty?: number
}

export interface VariantUpdatePayload {
  color?: string
  price_usd?: number
  cost_acquisition_usd?: number
  stock_qty?: number
  is_active?: boolean
}

export interface StockAdjustment {
  delta: number
  reason?: string
}

export interface StockAdjustmentResponse {
  variant_id: string
  previous_qty: number
  new_qty: number
  delta: number
}

export interface LowStockVariant {
  id: string
  sku: string
  style: ProductStyle
  size: ProductSize
  color: string
  stock_qty: number
  price_usd: string
  is_active: boolean
  images: ProductImage[]
}
