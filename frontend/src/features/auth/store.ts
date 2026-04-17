import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiClient } from '@shared/api/client'
import { authClient } from './auth-client'

const TOKEN_KEY = 'neon_auth_token'
const ROLE_KEY = 'neon_auth_role'

export const useAuthStore = defineStore('auth', () => {
  const role = ref<string | null>(localStorage.getItem(ROLE_KEY))

  const isAuthenticated = computed(() => !!localStorage.getItem(TOKEN_KEY))
  const isAdmin = computed(() => !!role.value && ['Owner', 'Operative'].includes(role.value))

  /**
   * Called on app startup. Syncs the stored access token with Neon Auth's
   * current session (handles auto-refresh) and fetches the admin role if applicable.
   */
  async function syncFromNeonAuth(): Promise<void> {
    try {
      const { data } = await authClient.getSession()
      if (!data) {
        clearAuth()
        return
      }
      const token = data.session.token
      localStorage.setItem(TOKEN_KEY, token)
      // Only fetch role if we don't already have one cached.
      // fetchRole errors are handled silently — a 401/403 here just means
      // the user is not an admin, and won't trigger the global redirect.
      if (!role.value) {
        await fetchRole()
      }
    } catch {
      // Network error or SDK failure — don't clear auth, just leave state as-is.
    }
  }

  /**
   * Fetches the current user's admin role from the backend.
   * Stores as 'Owner' or 'Operative' (capitalized). Clears role for non-admins.
   */
  async function fetchRole(): Promise<void> {
    try {
      const { data } = await apiClient.get<{ role: string }>('/users/me')
      const capitalised = data.role.charAt(0).toUpperCase() + data.role.slice(1)
      role.value = capitalised
      localStorage.setItem(ROLE_KEY, capitalised)
    } catch {
      role.value = null
      localStorage.removeItem(ROLE_KEY)
    }
  }

  /**
   * Sign in with email + password via Neon Auth.
   * Stores the access token and fetches the admin role.
   */
  async function login(email: string, password: string): Promise<void> {
    const { data, error } = await authClient.signIn.email({ email, password })
    if (error) throw new Error(error.message)
    const token = data?.token
    if (!token) throw new Error('Sign-in succeeded but no access token returned')
    localStorage.setItem(TOKEN_KEY, token)
    await fetchRole()
  }

  /**
   * Sign out from Neon Auth and clear all local auth state.
   */
  async function logout(): Promise<void> {
    try {
      await authClient.signOut()
    } catch {
      // ignore SDK errors on signOut
    }
    clearAuth()
  }

  function clearAuth(): void {
    role.value = null
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(ROLE_KEY)
  }

  return { role, isAuthenticated, isAdmin, login, logout, syncFromNeonAuth, clearAuth, fetchRole }
})
