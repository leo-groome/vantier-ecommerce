<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, RouterLink } from 'vue-router'

const route = useRoute()
const sidebarCollapsed = ref(false)

const navItems = [
  { to: '/admin/dashboard', label: 'Dashboard',   icon: 'M3 13l2-2m0 0l7-7 7 7M5 11v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' },
  { to: '/admin/inventory',  label: 'Inventory',   icon: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4' },
  { to: '/admin/orders',     label: 'Orders',      icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2' },
  { to: '/admin/purchases',  label: 'Purchases',   icon: 'M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z' },
  { to: '/admin/discounts',  label: 'Discounts',   icon: 'M7 7h.01M17 17h.01M8.5 4h7a1.5 1.5 0 011.5 1.5v13l-8-4-8 4V5.5A1.5 1.5 0 018.5 4z M9 9a3 3 0 100 6 3 3 0 000-6z' },
  { to: '/admin/finances',   label: 'Financials',  icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' },
  { to: '/admin/users',      label: 'Users',       icon: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z' },
]

function isActive(to: string) {
  return route.path.startsWith(to)
}

function clearAuth() {
  localStorage.removeItem('neon_auth_token')
  localStorage.removeItem('neon_auth_role')
  window.location.href = '/auth/login'
}
</script>

<template>
  <div class="min-h-screen flex bg-[color:var(--color-warm-beige)] text-[color:var(--color-on-surface)]">

    <!-- Sidebar -->
    <aside
      class="flex flex-col border-r border-[color:var(--color-border)] bg-[color:var(--color-obsidian)] transition-[width] duration-[var(--duration-slow)] ease-[var(--ease-out-expo)]"
      :class="sidebarCollapsed ? 'w-16' : 'w-56'"
    >
      <!-- Brand -->
      <div class="h-16 flex items-center px-4 border-b border-white/10 flex-shrink-0">
        <RouterLink to="/" class="flex items-center gap-3 overflow-hidden">
          <span class="text-[color:var(--color-ivory)] font-bold uppercase tracking-[var(--tracking-display)] text-[length:var(--text-micro)] flex-shrink-0">V</span>
          <span
            class="text-[color:var(--color-ivory)] font-bold uppercase tracking-[var(--tracking-display)] text-[length:var(--text-micro)] whitespace-nowrap transition-[opacity,width] duration-[var(--duration-normal)]"
            :class="sidebarCollapsed ? 'opacity-0 w-0' : 'opacity-100'"
          >
            Vantier
          </span>
        </RouterLink>
        <button
          class="ml-auto text-white/40 hover:text-white/80 transition-colors duration-[var(--duration-fast)] flex-shrink-0"
          :aria-label="sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
          @click="sidebarCollapsed = !sidebarCollapsed"
        >
          <svg class="w-4 h-4 transition-transform duration-[var(--duration-normal)]" :class="sidebarCollapsed ? 'rotate-180' : ''" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <polyline points="15 18 9 12 15 6"/>
          </svg>
        </button>
      </div>

      <!-- Nav -->
      <nav class="flex-1 py-4 overflow-hidden">
        <RouterLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="flex items-center gap-3 px-4 py-2.5 mx-2 rounded-[var(--radius-md)] text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] transition-colors duration-[var(--duration-fast)] group"
          :class="isActive(item.to)
            ? 'bg-white/10 text-[color:var(--color-ivory)]'
            : 'text-white/50 hover:text-white/80 hover:bg-white/5'"
        >
          <svg class="w-4 h-4 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path :d="item.icon" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span
            class="whitespace-nowrap transition-[opacity,width] duration-[var(--duration-normal)] overflow-hidden"
            :class="sidebarCollapsed ? 'opacity-0 w-0' : 'opacity-100'"
          >
            {{ item.label }}
          </span>
          <!-- Active dot when collapsed -->
          <span v-if="sidebarCollapsed && isActive(item.to)" class="absolute right-1 w-1.5 h-1.5 rounded-full bg-[color:var(--color-amber-accent)]" />
        </RouterLink>
      </nav>

      <!-- Footer: storefront link + logout -->
      <div class="border-t border-white/10 py-4 px-2 space-y-1 flex-shrink-0">
        <RouterLink
          to="/"
          target="_blank"
          class="flex items-center gap-3 px-3 py-2 text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-white/40 hover:text-white/70 transition-colors duration-[var(--duration-fast)] rounded-[var(--radius-md)]"
        >
          <svg class="w-4 h-4 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span :class="sidebarCollapsed ? 'opacity-0 w-0 overflow-hidden' : 'opacity-100'">Storefront</span>
        </RouterLink>
        <button
          class="w-full flex items-center gap-3 px-3 py-2 text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-white/40 hover:text-white/70 transition-colors duration-[var(--duration-fast)] rounded-[var(--radius-md)]"
          @click="clearAuth"
        >
          <svg class="w-4 h-4 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span :class="sidebarCollapsed ? 'opacity-0 w-0 overflow-hidden' : 'opacity-100'">Logout</span>
        </button>
      </div>
    </aside>

    <!-- Main content -->
    <div class="flex-1 flex flex-col min-w-0">
      <!-- Top bar -->
      <header class="h-16 border-b border-[color:var(--color-border)] bg-[color:var(--color-ivory)] flex items-center px-6 gap-4 flex-shrink-0">
        <div class="flex-1">
          <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-border-strong)]">
            Admin Panel
          </p>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-7 h-7 rounded-full bg-[color:var(--color-obsidian)] flex items-center justify-center text-[color:var(--color-ivory)] text-[10px] font-bold">
            O
          </div>
          <span class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-border-strong)]">Owner</span>
        </div>
      </header>

      <!-- Page content -->
      <main class="flex-1 overflow-y-auto p-6">
        <RouterView />
      </main>
    </div>
  </div>
</template>
