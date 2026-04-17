import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'

function getToken(): string | null {
  return localStorage.getItem('neon_auth_token')
}

function getUserRole(): string | null {
  return localStorage.getItem('neon_auth_role')
}

function getCartCount(): number {
  try {
    const cart = JSON.parse(localStorage.getItem('vantier_cart') ?? '[]')
    if (!Array.isArray(cart)) return 0
    return cart.reduce((sum: number, item: { quantity?: number }) => sum + (item.quantity ?? 1), 0)
  } catch {
    return 0
  }
}

export function applyRouteGuards(
  to: RouteLocationNormalized,
  _from: RouteLocationNormalized,
  next: NavigationGuardNext
): void {
  const meta = to.meta

  // Already authenticated admin visiting the login page → go to dashboard
  if (meta.guestOnly && getToken() && getUserRole()) {
    next({ path: '/admin/dashboard' })
    return
  }

  if (meta.requireAuth && !getToken()) {
    next({ path: '/auth/login', query: { redirect: to.fullPath } })
    return
  }

  if (meta.requireAdmin) {
    const role = getUserRole()
    if (!role || !['Owner', 'Operative'].includes(role)) {
      next({ path: '/auth/login', query: { redirect: to.fullPath } })
      return
    }
  }

  if (meta.requireOwner) {
    const role = getUserRole()
    if (role !== 'Owner') {
      next({ path: '/admin/dashboard' })
      return
    }
  }

  if (meta.requireCart && getCartCount() === 0) {
    next({ path: '/cart' })
    return
  }

  next()
}
