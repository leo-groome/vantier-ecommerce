export type POStatus = 'ordered' | 'in_transit' | 'received'

export interface POItem {
  id: string
  po_id: string
  variant_id: string
  qty_ordered: number
  qty_received: number
  created_at: string
}

export interface PurchaseOrder {
  id: string
  reference_number: string
  supplier_name: string
  expected_arrival_date: string | null
  status: POStatus
  notes: string | null
  created_by_user_id: string | null
  items: POItem[]
  created_at: string
  updated_at: string
}

export interface POCreatePayload {
  reference_number: string
  supplier_name: string
  expected_arrival_date?: string
  notes?: string
  items: { variant_id: string; qty_ordered: number }[]
}
