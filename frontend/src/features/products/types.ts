export interface ProductImage {
  id: string
  url: string
  alt: string
  isPrimary: boolean
}

export interface ProductVariant {
  id: string
  size: string
  color: string
  stock: number
  sku: string
}

export interface Product {
  id: string
  name: string
  line: 'Polo Atelier' | 'Signature' | 'Essential'
  style: 'Classic' | 'Design'
  priceUSD: number
  images: ProductImage[]
  variants: ProductVariant[]
}

export interface ProductFilters {
  line?: Product['line']
  style?: Product['style']
  size?: string
  color?: string
}
