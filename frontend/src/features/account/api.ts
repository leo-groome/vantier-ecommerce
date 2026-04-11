import { apiClient } from '@shared/api/client'
import type { User, SavedAddress } from './types'

export async function fetchProfile(): Promise<User> {
  const { data } = await apiClient.get<User>('/users/me')
  return data
}

export async function fetchSavedAddresses(): Promise<SavedAddress[]> {
  const { data } = await apiClient.get<SavedAddress[]>('/inventory/addresses')
  return data
}
