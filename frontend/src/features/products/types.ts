// Backend enum values (snake_case) — used in API requests/responses
export type ProductLine = 'polo_atelier' | 'signature' | 'essential'
export type ProductStyle = 'classic' | 'design'
export type ProductSize = 'S' | 'M' | 'L' | 'XL' | 'XXL' | 'XXXL'

// Display labels for UI
export const LINE_LABELS: Record<ProductLine, string> = {
  polo_atelier: 'Polo Atelier',
  signature: 'Signature',
  essential: 'Essential',
}

export const STYLE_LABELS: Record<ProductStyle, string> = {
  classic: 'Classic',
  design: 'Design',
}

export interface ProductImage {
  id: string
  url: string
  alt_text: string | null
  position: number
}

export interface ProductVariant {
  id: string
  sku: string
  style: ProductStyle
  size: ProductSize
  color: string
  stock_qty: number
  price_usd: string  // Decimal from backend comes as string
  is_active: boolean
  images: ProductImage[]
}

export interface Product {
  id: string
  name: string
  line: ProductLine
  description: string | null
  is_active: boolean
  variants: ProductVariant[]
}

export interface ProductListResponse {
  items: Product[]
  total: number
  page: number
  page_size: number
}

export interface ProductFilters {
  line?: ProductLine
  style?: ProductStyle
  size?: ProductSize
  color?: string
  in_stock?: boolean
}
