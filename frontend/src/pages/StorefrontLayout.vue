<script setup lang="ts">
import { ref } from 'vue'
import { useCartStore } from '@features/cart/store'
import CartDrawer from '@features/cart/components/CartDrawer.vue'

const cart = useCartStore()
const mobileMenuOpen = ref(false)
const cartOpen = ref(false)
</script>
<template>
  <div class="min-h-screen flex flex-col bg-[color:var(--color-surface)] text-[color:var(--color-on-surface)]">
    <!-- Nav -->
    <header class="sticky top-0 z-40 border-b border-[color:var(--color-border)] bg-[color:var(--color-surface)]/95 backdrop-blur-sm">
      <div class="max-w-[var(--container-max)] mx-auto px-[var(--spacing-container)] h-16 flex items-center justify-between">
        <!-- Logo -->
        <RouterLink
          to="/"
          class="text-[length:var(--text-small)] font-bold uppercase tracking-[var(--tracking-display)] text-[color:var(--color-on-surface)] hover:opacity-70 transition-opacity duration-[var(--duration-fast)]"
        >
          Vantier
        </RouterLink>

        <!-- Nav links -->
        <nav class="hidden md:flex items-center gap-8" aria-label="Main navigation">
          <RouterLink
            v-for="link in [{ to: '/', label: 'Home' }, { to: '/shop', label: 'Shop' }, { to: '/about', label: 'About' }]"
            :key="link.to"
            :to="link.to"
            class="text-[length:var(--text-small)] font-medium uppercase tracking-[var(--tracking-label)] relative after:absolute after:bottom-0 after:left-0 after:h-px after:bg-current after:transition-[width] after:duration-[var(--duration-normal)] after:ease-[var(--ease-out-expo)] hover:after:w-full"
            :class="$route.path === link.to ? 'after:w-full' : 'after:w-0'"
          >
            {{ link.label }}
          </RouterLink>
        </nav>

        <!-- Right actions -->
        <div class="flex items-center gap-4">
          <!-- Cart icon -->
          <button class="relative p-2 hover:opacity-70 transition-opacity duration-[var(--duration-fast)]" aria-label="Open cart" @click="cartOpen = true">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/>
            </svg>
            <Transition name="badge-pop">
              <span
                v-if="cart.totalItems > 0"
                :key="cart.totalItems"
                class="absolute -top-0.5 -right-0.5 w-4 h-4 rounded-full bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-[10px] font-bold flex items-center justify-center"
              >
                {{ cart.totalItems > 9 ? '9+' : cart.totalItems }}
              </span>
            </Transition>
          </button>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main class="flex-1">
      <RouterView />
    </main>

    <!-- Footer -->
    <footer class="border-t border-[color:var(--color-border)] mt-[var(--spacing-section)]">
      <div class="max-w-[var(--container-max)] mx-auto px-[var(--spacing-container)] py-12">
        <div class="flex flex-col md:flex-row items-center justify-between gap-6">
          <p class="text-[length:var(--text-small)] font-bold uppercase tracking-[var(--tracking-display)]">Vantier</p>
          <nav class="flex gap-6 text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-60">
            <RouterLink to="/contact" class="hover:opacity-100 transition-opacity">Contact</RouterLink>
            <RouterLink to="/contact" class="hover:opacity-100 transition-opacity">Exchange Policy</RouterLink>
            <RouterLink to="/contact" class="hover:opacity-100 transition-opacity">Shipping</RouterLink>
          </nav>
          <p class="text-[length:var(--text-micro)] opacity-40">© {{ new Date().getFullYear() }} Vantier</p>
        </div>
      </div>
    </footer>
  </div>

  <!-- Badge pop animation -->
  <style>
  .badge-pop-enter-active { transition: transform var(--duration-normal) var(--ease-out-expo); }
  .badge-pop-enter-from { transform: scale(1.4); }
  .badge-pop-enter-to { transform: scale(1); }
  </style>

  <!-- Cart Drawer (teleported to body to escape stacking contexts) -->
  <Teleport to="body">
    <CartDrawer :open="cartOpen" @close="cartOpen = false" />
  </Teleport>
</template>
