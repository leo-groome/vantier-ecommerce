export type ExchangeStatus = 'requested' | 'approved' | 'shipped' | 'completed'

export interface Exchange {
  id: string
  originalOrderId: string
  originalVariantId: string
  requestedVariantId: string
  status: ExchangeStatus
  createdAt: string
}
