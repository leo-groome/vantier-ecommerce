import { apiClient } from '@shared/api/client'
import type { AdminUser, AdminRole, InviteUserPayload } from './types'

export async function listUsers(): Promise<AdminUser[]> {
  const { data } = await apiClient.get<AdminUser[]>('/users')
  return data
}

export async function inviteUser(payload: InviteUserPayload): Promise<AdminUser> {
  const { data } = await apiClient.post<AdminUser>('/users', payload)
  return data
}

export async function updateUserRole(id: string, role: AdminRole): Promise<AdminUser> {
  const { data } = await apiClient.patch<AdminUser>(`/users/${id}`, { role })
  return data
}

export async function removeUser(id: string): Promise<void> {
  await apiClient.delete(`/users/${id}`)
}
