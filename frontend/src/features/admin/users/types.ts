export type AdminRole = 'owner' | 'operative'

export interface AdminUser {
  id: string
  neon_auth_user_id: string | null
  email: string
  role: AdminRole
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface InviteUserPayload {
  email: string
  role: AdminRole
}
