import axios, { type AxiosInstance } from 'axios'
import { authClient } from '@features/auth/auth-client'

export const apiClient: AxiosInstance = axios.create({
  baseURL: (import.meta.env.VITE_API_URL ?? 'http://localhost:8000') + '/api/v1',
  timeout: 15_000,
})

// Inject a fresh Neon Auth JWT before every request.
// authClient.getSession() auto-refreshes if the stored token is expired.
apiClient.interceptors.request.use(async (config) => {
  let token: string | null = null
  try {
    const sessionTimeout = new Promise<never>((_, reject) =>
      setTimeout(() => reject(new Error('session timeout')), 5_000)
    )
    const { data } = await Promise.race([authClient.getSession(), sessionTimeout])
    if (data) {
      token = data.session.token
      localStorage.setItem('neon_auth_token', token)
    }
  } catch {
    token = localStorage.getItem('neon_auth_token')
  }
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle auth errors globally.
// Only redirect on 401 if NOT already on an auth page (prevents infinite reload loop).
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && !window.location.pathname.startsWith('/auth')) {
      window.location.href = '/auth/login'
    }
    return Promise.reject(error)
  }
)
