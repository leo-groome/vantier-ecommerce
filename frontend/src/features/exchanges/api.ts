import { apiClient } from '@shared/api/client'
import type { Exchange } from './types'

export async function fetchExchanges(): Promise<Exchange[]> {
  const { data } = await apiClient.get<Exchange[]>('/exchanges')
  return data
}

export async function requestExchange(payload: {
  originalOrderId: string
  originalVariantId: string
  requestedVariantId: string
}): Promise<Exchange> {
  const { data } = await apiClient.post<Exchange>('/exchanges', payload)
  return data
}
