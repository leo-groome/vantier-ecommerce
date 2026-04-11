export interface OrderItem {
  productId: string
  variantId: string
  name: string
  size: string
  color: string
  priceUSD: number
  quantity: number
}

export type OrderStatus = 'pending' | 'confirmed' | 'shipped' | 'delivered'

export interface Order {
  id: string
  status: OrderStatus
  items: OrderItem[]
  totalUSD: number
  shippingUSD: number
  discountUSD: number
  createdAt: string
  trackingNumber?: string
}
