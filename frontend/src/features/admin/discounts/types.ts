export type DiscountType = 'percent' | 'fixed'

export interface DiscountCode {
  id: string
  code: string
  type: DiscountType
  value: number
  usage_limit: number | null
  usage_count: number
  expires_at: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface DiscountCreatePayload {
  code: string
  type: DiscountType
  value: number
  usage_limit?: number
  expires_at?: string
}

export interface DiscountUpdatePayload {
  usage_limit?: number | null
  expires_at?: string | null
  is_active?: boolean
}
