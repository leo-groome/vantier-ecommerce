export type OrderStatus = 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled'

export interface OrderShippingAddress {
  full_name: string
  line1: string
  line2?: string
  city: string
  state: string
  zip: string
  country: string
  phone?: string
}

export interface AdminOrderItem {
  id: string
  variant_id: string
  qty: number
  unit_price_usd: string
}

export interface AdminOrder {
  id: string
  customer_email: string
  customer_name: string | null
  status: OrderStatus
  payment_status: string
  subtotal_usd: string
  shipping_usd: string
  discount_usd: string
  total_usd: string
  is_free_shipping: boolean
  shipping_address: OrderShippingAddress
  carrier_tracking_number: string | null
  envia_label_url: string | null
  items: AdminOrderItem[]
  created_at: string
  updated_at: string
}

export interface AdminOrderListResponse {
  items: AdminOrder[]
  total: number
  page: number
  page_size: number
}

export interface OrderFilters {
  status?: OrderStatus | 'all'
  customer_email?: string
  page?: number
  page_size?: number
}
