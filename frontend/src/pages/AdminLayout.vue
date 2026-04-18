<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@features/auth/store'
import { useAdminInventoryStore } from '@features/admin/inventory/store'

const route  = useRoute()
const router = useRouter()
const auth   = useAuthStore()
const inventory = useAdminInventoryStore()

const sidebarCollapsed = ref(false)
const userName = ref<string | null>(null)

// Try to get display name from Neon Auth session
onMounted(async () => {
  try {
    const { authClient } = await import('@features/auth/auth-client')
    const { data } = await authClient.getSession()
    if (data) {
      const user = (data as any).user ?? (data as any).session?.user
      userName.value = user?.displayName ?? user?.primaryEmail?.split('@')[0] ?? null
    }
  } catch { /* fallback to role */ }
  // Also ensure inventory is loaded for badge count
  if (!inventory.products.length) inventory.loadProducts()
})

const lowStockCount = computed(() =>
  inventory.products.reduce(
    (n, p) => n + p.variants.filter(v => v.is_active && v.stock_qty <= 15).length, 0
  )
)

interface NavItem  { to: string; label: string; icon: string; badge?: number }
interface NavGroup { label: string; items: NavItem[] }

const navGroups = computed<NavGroup[]>(() => [
  {
    label: 'Principal',
    items: [
      {
        to: '/admin/dashboard', label: 'Dashboard',
        icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6',
      },
      {
        to: '/admin/inventory', label: 'Inventario',
        icon: 'M20 7H4a2 2 0 00-2 2v6a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2zM16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16',
        badge: lowStockCount.value || undefined,
      },
      {
        to: '/admin/orders', label: 'Órdenes',
        icon: 'M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4zM3 6h18M16 10a4 4 0 01-8 0',
      },
      {
        to: '/admin/purchases', label: 'Compras',
        icon: 'M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z',
      },
    ],
  },
  {
    label: 'Finanzas',
    items: [
      {
        to: '/admin/discounts', label: 'Descuentos',
        icon: 'M12 1v22M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6',
      },
      {
        to: '/admin/finances', label: 'Financiero',
        icon: 'M22 12h-4l-3 9L9 3l-3 9H2',
      },
    ],
  },
  {
    label: 'Sistema',
    items: [
      {
        to: '/admin/users', label: 'Usuarios',
        icon: 'M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2M9 7a4 4 0 100 8 4 4 0 000-8zM23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75',
      },
    ],
  },
])

const ROUTE_TITLES: Record<string, string> = {
  '/admin/dashboard':  'Dashboard',
  '/admin/inventory':  'Inventario',
  '/admin/orders':     'Órdenes',
  '/admin/purchases':  'Compras',
  '/admin/discounts':  'Descuentos',
  '/admin/finances':   'Financiero',
  '/admin/users':      'Usuarios',
}

const pageTitle = computed(() => {
  for (const key of Object.keys(ROUTE_TITLES)) {
    if (route.path.startsWith(key)) return ROUTE_TITLES[key]
  }
  return 'Admin'
})

const pageCrumb = computed(() => {
  const crumbs: Record<string, string> = {
    '/admin/dashboard': 'Vista general',
    '/admin/inventory': 'Productos · Variantes · Stock',
    '/admin/orders':    'Gestión de pedidos',
    '/admin/purchases': 'Proveedores · Reposición de stock',
    '/admin/discounts': 'Cupones y promociones',
    '/admin/finances':  'Rentabilidad · Analíticas avanzadas',
    '/admin/users':     'Acceso y roles',
  }
  for (const key of Object.keys(crumbs)) {
    if (route.path.startsWith(key)) return crumbs[key]
  }
  return ''
})

const userInitial = computed(() => {
  if (userName.value) {
    const parts = userName.value.trim().split(' ')
    return parts.length >= 2
      ? (parts[0][0] + parts[1][0]).toUpperCase()
      : parts[0][0].toUpperCase()
  }
  return auth.role?.charAt(0)?.toUpperCase() ?? 'A'
})

const displayName = computed(() => userName.value ?? auth.role ?? '—')

function isActive(to: string) {
  return route.path.startsWith(to)
}

async function clearAuth() {
  await auth.logout()
  await router.push('/auth/login')
}
</script>

<template>
  <div class="min-h-screen flex" style="background: var(--admin-bg);">

    <!-- ── SIDEBAR ─────────────────────────────────────────────── -->
    <aside
      class="flex flex-col flex-shrink-0 h-screen sticky top-0 transition-[width] duration-300 ease-out overflow-hidden"
      :style="{ width: sidebarCollapsed ? '64px' : '240px', background: 'var(--admin-sidebar-bg)', boxShadow: '4px 0 24px rgba(0,0,0,0.18)' }"
    >
      <!-- Brand -->
      <div
        class="flex items-center h-16 flex-shrink-0 gap-2 px-4 overflow-hidden"
        style="border-bottom: 1px solid rgba(255,255,255,0.07);"
      >
        <RouterLink to="/" class="flex-1 min-w-0 overflow-hidden" :class="sidebarCollapsed ? 'opacity-0 pointer-events-none' : 'opacity-100 transition-opacity duration-200'">
          <p class="font-bold uppercase tracking-[0.2em] text-white" style="font-size: 0.85rem; letter-spacing: 0.22em;">VANTIER</p>
          <p class="uppercase tracking-widest font-medium" style="font-size: 0.52rem; color: var(--admin-amber); letter-spacing: 0.2em;">Panel Administrativo</p>
        </RouterLink>
        <button
          class="flex-shrink-0 w-6 h-6 flex items-center justify-center transition-colors duration-150"
          style="color: rgba(255,255,255,0.35);"
          @click="sidebarCollapsed = !sidebarCollapsed"
        >
          <svg class="w-4 h-4 transition-transform duration-300" :class="sidebarCollapsed ? 'rotate-180' : ''" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="15 18 9 12 15 6"/>
          </svg>
        </button>
      </div>

      <!-- Nav -->
      <nav class="flex-1 overflow-y-auto overflow-x-hidden py-2">
        <template v-for="group in navGroups" :key="group.label">
          <!-- Group label -->
          <p
            v-if="!sidebarCollapsed"
            class="px-4 pt-4 pb-1.5 font-semibold uppercase select-none"
            style="font-size: 0.55rem; color: rgba(255,255,255,0.22); letter-spacing: 0.2em;"
          >{{ group.label }}</p>

          <RouterLink
            v-for="item in group.items"
            :key="item.to"
            :to="item.to"
            class="flex items-center gap-2.5 mx-2 my-0.5 rounded-lg transition-all duration-150 relative overflow-hidden"
            :class="sidebarCollapsed ? 'px-0 justify-center py-3' : 'px-3 py-2.5'"
            :style="isActive(item.to)
              ? { background: 'rgba(201,168,76,0.12)', color: 'var(--admin-amber)', borderLeft: sidebarCollapsed ? '3px solid transparent' : '3px solid var(--admin-amber)' }
              : { color: 'rgba(255,255,255,0.45)', borderLeft: '3px solid transparent' }"
          >
            <svg class="w-[17px] h-[17px] flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">
              <path :d="item.icon" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span
              v-if="!sidebarCollapsed"
              class="text-[0.72rem] font-medium flex-1 whitespace-nowrap overflow-hidden"
            >{{ item.label }}</span>
            <!-- Badge -->
            <span
              v-if="!sidebarCollapsed && item.badge"
              class="text-[0.58rem] font-bold px-1.5 py-0.5 rounded-full flex-shrink-0"
              style="background: rgba(201,168,76,0.2); color: var(--admin-amber);"
            >{{ item.badge }}</span>
          </RouterLink>
        </template>
      </nav>

      <!-- User card -->
      <div class="flex-shrink-0" style="border-top: 1px solid rgba(255,255,255,0.07);">
        <template v-if="!sidebarCollapsed">
          <div class="p-4 space-y-3">
            <div class="flex items-center gap-2.5">
              <div
                class="w-8 h-8 rounded-full flex items-center justify-center text-[0.65rem] font-bold flex-shrink-0"
                style="background: linear-gradient(135deg, var(--admin-amber), #a07820); color: #fff; box-shadow: 0 2px 8px rgba(201,168,76,0.3);"
              >{{ userInitial }}</div>
              <div class="min-w-0 flex-1">
                <p class="text-[0.78rem] font-semibold text-white truncate">{{ displayName }}</p>
                <p class="text-[0.58rem] uppercase font-medium tracking-widest" style="color: var(--admin-amber);">{{ auth.role ?? '' }}</p>
              </div>
            </div>
            <div class="flex gap-4 text-[0.65rem] uppercase tracking-wider pl-0.5">
              <RouterLink
                to="/"
                class="transition-colors duration-150 flex items-center gap-1"
                style="color: rgba(255,255,255,0.35);"
              >
                <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z" stroke-linecap="round"/>
                </svg>
                Ver tienda
              </RouterLink>
              <button
                class="transition-colors duration-150 flex items-center gap-1"
                style="color: rgba(255,255,255,0.35);"
                @click="clearAuth"
              >
                <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Cerrar sesión
              </button>
            </div>
          </div>
        </template>
        <template v-else>
          <div class="p-3 flex flex-col items-center gap-2">
            <div
              class="w-8 h-8 rounded-full flex items-center justify-center text-[0.65rem] font-bold cursor-pointer"
              style="background: linear-gradient(135deg, var(--admin-amber), #a07820); color: #fff;"
              @click="clearAuth"
            >{{ userInitial }}</div>
          </div>
        </template>
      </div>
    </aside>

    <!-- ── MAIN AREA ───────────────────────────────────────────── -->
    <div class="flex-1 flex flex-col min-w-0">

      <!-- Topbar -->
      <header
        class="h-[58px] flex items-center px-6 gap-6 flex-shrink-0 bg-white z-10"
        style="box-shadow: 0 1px 0 rgba(0,0,0,0.06), 0 2px 8px rgba(0,0,0,0.04);"
      >
        <div class="flex-1 min-w-0">
          <p class="text-[1rem] font-bold truncate" style="color: var(--admin-text-primary); letter-spacing: -0.01em;">{{ pageTitle }}</p>
          <p class="text-[0.68rem]" style="color: var(--admin-text-secondary);">{{ pageCrumb }}</p>
        </div>
        <div class="flex items-center gap-1 flex-shrink-0">
          <!-- Search -->
          <button
            class="w-9 h-9 flex items-center justify-center rounded-lg transition-colors duration-150"
            style="color: var(--admin-text-secondary);"
          >
            <svg class="w-[18px] h-[18px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35" stroke-linecap="round"/>
            </svg>
          </button>
          <!-- Bell -->
          <button
            class="w-9 h-9 flex items-center justify-center rounded-lg transition-colors duration-150"
            style="color: var(--admin-text-secondary);"
          >
            <svg class="w-[18px] h-[18px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6 6 0 10-12 0v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <!-- Avatar -->
          <div
            class="w-8 h-8 rounded-full flex items-center justify-center text-[0.65rem] font-bold ml-1 cursor-default"
            style="background: linear-gradient(135deg, var(--admin-amber), #a07820); color: #fff;"
          >{{ userInitial }}</div>
        </div>
      </header>

      <!-- Page content -->
      <main class="flex-1 overflow-y-auto p-6">
        <RouterView />
      </main>
    </div>
  </div>
</template>
