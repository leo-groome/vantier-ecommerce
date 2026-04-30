<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@features/auth/store'
import { useAdminInventoryStore } from '@features/admin/inventory/store'

const route  = useRoute()
const router = useRouter()
const auth   = useAuthStore()
const inventory = useAdminInventoryStore()

const sidebarCollapsed = ref(true) // Start collapsed by default for the hover effect
const isHovered        = ref(false)
const showUserMenu     = ref(false)

const isCompact = computed(() => sidebarCollapsed.value && !isHovered.value)

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
    label: '',
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
        to: '/admin/discounts', label: 'Descuentos',
        icon: 'M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z',
      },
      {
        to: '/admin/finances', label: 'Financiero',
        icon: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
      },
      {
        to: '/admin/users', label: 'Usuarios',
        icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197',
      },
      {
        to: '/admin/homepage', label: 'Config. Main',
        icon: 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z',
      },
    ],
  },
])

const ROUTE_TITLES: Record<string, string> = {
  '/admin/dashboard':  'Dashboard',
  '/admin/inventory':  'Inventario',
  '/admin/orders':     'Órdenes',
  '/admin/discounts':  'Descuentos',
  '/admin/finances':   'Financiero',
  '/admin/users':      'Usuarios',
  '/admin/homepage':   'Configuración Main',
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
    '/admin/discounts': 'Cupones y promociones',
    '/admin/finances':  'Rentabilidad · Analíticas avanzadas',
    '/admin/users':     'Acceso y roles',
    '/admin/homepage':  'Hero · Colecciones · Imágenes',
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
  <div class="h-screen flex overflow-hidden" style="background: var(--admin-bg);">

    <!-- ── SIDEBAR ─────────────────────────────────────────────── -->
    <aside
      @mouseenter="isHovered = true"
      @mouseleave="isHovered = false"
      class="flex flex-col flex-shrink-0 h-full relative transition-[width] duration-300 ease-out z-20"
      :style="{ width: isCompact ? '64px' : '260px', background: '#ffffff', borderRight: '1px solid rgba(0,0,0,0.06)', boxShadow: '4px 0 24px rgba(0,0,0,0.02)' }"
    >
      <!-- Brand -->
      <div
        class="flex items-center h-[58px] flex-shrink-0 px-4 whitespace-nowrap relative"
        style="border-bottom: 1px solid rgba(0,0,0,0.06);"
      >
        <RouterLink to="/" class="flex-1 flex items-center justify-center transition-opacity duration-300" :class="isCompact ? 'opacity-0 pointer-events-none' : 'opacity-100'">
          <img src="/Logos y tipografia/LOGOTIPO NEGRO VANTIER.svg" alt="Vantier" class="h-4 object-contain" />
        </RouterLink>
        <button
          class="flex-shrink-0 w-6 h-6 flex items-center justify-center transition-colors duration-150 absolute right-4"
          style="color: var(--admin-text-secondary);"
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
            v-if="!isCompact && group.label"
            class="px-4 pt-4 pb-1.5 font-bold uppercase select-none transition-opacity duration-300"
            style="font-size: 0.55rem; color: var(--admin-text-secondary); opacity: 0.6; letter-spacing: 0.15em;"
          >{{ group.label }}</p>

          <RouterLink
            v-for="item in group.items"
            :key="item.to"
            :to="item.to"
            class="flex items-center gap-4 mx-3 my-0.5 rounded-xl transition-all duration-150 relative overflow-hidden h-11"
            :class="isCompact ? 'px-0 justify-center' : 'px-4 hover:bg-black/[0.02]'"
            :style="isActive(item.to)
              ? { background: 'rgba(201,168,76,0.08)', color: 'var(--admin-amber)', borderLeft: isCompact ? '4px solid transparent' : '4px solid var(--admin-amber)' }
              : { color: 'var(--admin-text-secondary)', borderLeft: '4px solid transparent' }"
          >
            <svg class="w-[19px] h-[19px] flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path :d="item.icon" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span
              v-if="!isCompact"
              class="text-[0.78rem] font-semibold flex-1 whitespace-nowrap overflow-hidden transition-opacity duration-300"
              :style="{ color: isActive(item.to) ? 'var(--admin-amber)' : 'var(--admin-text-primary)' }"
            >{{ item.label }}</span>
            <!-- Badge -->
            <span
              v-if="!isCompact && item.badge"
              class="text-[0.62rem] font-bold px-2 py-0.5 rounded-full flex-shrink-0"
              style="background: rgba(201,168,76,0.15); color: var(--admin-amber);"
            >{{ item.badge }}</span>
          </RouterLink>
        </template>
      </nav>
    </aside>

    <!-- ── MAIN AREA ───────────────────────────────────────────── -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden">

      <!-- Topbar -->
      <header
        class="h-[58px] flex items-center px-6 gap-6 flex-shrink-0 bg-white z-10"
        style="box-shadow: 0 1px 0 rgba(0,0,0,0.06), 0 2px 8px rgba(0,0,0,0.04);"
      >
        <div class="flex-1 min-w-0">
          <p class="text-[1.1rem] font-bold truncate" style="font-family: var(--font-sans); color: var(--admin-text-primary); letter-spacing: -0.01em;">{{ pageTitle }}</p>
          <p class="text-[0.68rem] font-medium uppercase tracking-widest opacity-60" style="font-family: var(--font-sans); color: var(--admin-text-secondary);">{{ pageCrumb }}</p>
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

          <!-- Avatar with Dropdown -->
          <div class="relative ml-1">
            <button
              @click="showUserMenu = !showUserMenu"
              class="w-8 h-8 rounded-full flex items-center justify-center text-[0.65rem] font-bold transition-transform hover:scale-105 active:scale-95 shadow-sm"
              style="background: linear-gradient(135deg, var(--admin-amber), #a07820); color: #fff;"
            >
              {{ userInitial }}
            </button>

            <!-- Dropdown Menu -->
            <div v-if="showUserMenu" class="fixed inset-0 z-40" @click="showUserMenu = false"></div>
            <Transition name="fade-in-up">
              <div
                v-if="showUserMenu"
                class="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-2xl border border-black/5 py-2 z-50 transform origin-top-right overflow-hidden"
                style="box-shadow: 0 10px 40px -10px rgba(0,0,0,0.15);"
              >
                <div class="px-4 py-2 border-b border-black/[0.03] mb-1">
                  <p class="text-[0.75rem] font-bold truncate" style="color: var(--admin-text-primary);">{{ displayName }}</p>
                  <p class="text-[0.55rem] uppercase font-bold tracking-widest" style="color: var(--admin-amber);">{{ auth.role ?? '' }}</p>
                </div>
                
                <RouterLink
                  to="/"
                  class="flex items-center gap-2.5 px-4 py-2 text-[0.72rem] transition-colors hover:bg-black/[0.03]"
                  style="color: var(--admin-text-primary);"
                  @click="showUserMenu = false"
                >
                  <svg class="w-4 h-4 opacity-60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/>
                  </svg>
                  Ver tienda
                </RouterLink>

                <button
                  class="w-full flex items-center gap-2.5 px-4 py-2 text-[0.72rem] transition-colors hover:bg-red-50"
                  style="color: #ef4444;"
                  @click="clearAuth"
                >
                  <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  Cerrar sesión
                </button>
              </div>
            </Transition>
          </div>
        </div>
      </header>

      <!-- Page content -->
      <main class="flex-1 overflow-y-auto p-6">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<style scoped>
.fade-in-up-enter-active {
  transition: all 0.2s ease-out;
}
.fade-in-up-leave-active {
  transition: all 0.15s ease-in;
}
.fade-in-up-enter-from {
  opacity: 0;
  transform: translateY(10px) scale(0.95);
}
.fade-in-up-leave-to {
  opacity: 0;
  transform: translateY(10px) scale(0.95);
}
</style>
