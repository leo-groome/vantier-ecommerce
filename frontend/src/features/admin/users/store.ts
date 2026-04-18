import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as api from './api'
import type { AdminUser, AdminRole, InviteUserPayload } from './types'

export const useAdminUsersStore = defineStore('admin/users', () => {
  const users = ref<AdminUser[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function loadUsers() {
    loading.value = true
    error.value = null
    try {
      users.value = await api.listUsers()
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Error al cargar usuarios'
    } finally {
      loading.value = false
    }
  }

  async function invite(payload: InviteUserPayload): Promise<AdminUser | null> {
    try {
      const user = await api.inviteUser(payload)
      users.value.push(user)
      return user
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Error al invitar usuario'
      return null
    }
  }

  async function changeRole(id: string, role: AdminRole): Promise<boolean> {
    try {
      const updated = await api.updateUserRole(id, role)
      const idx = users.value.findIndex(u => u.id === id)
      if (idx !== -1) users.value[idx] = updated
      return true
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Error al cambiar rol'
      return false
    }
  }

  async function deactivate(id: string): Promise<boolean> {
    try {
      await api.removeUser(id)
      const idx = users.value.findIndex(u => u.id === id)
      if (idx !== -1) users.value[idx].is_active = false
      return true
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Error al desactivar usuario'
      return false
    }
  }

  return { users, loading, error, loadUsers, invite, changeRole, deactivate }
})
