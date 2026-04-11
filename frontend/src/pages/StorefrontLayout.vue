<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useCartStore } from '@features/cart/store'
import CartDrawer from '@features/cart/components/CartDrawer.vue'
import ToastContainer from '@shared/components/ToastContainer.vue'

const route = useRoute()
const cart = useCartStore()
const mobileMenuOpen = ref(false)
const cartOpen = ref(false)

// Close mobile menu on route change
watch(() => route.path, () => { mobileMenuOpen.value = false })

const navLinks = [
  { to: '/', label: 'Home' },
  { to: '/shop', label: 'Shop' },
  { to: '/about', label: 'About' },
]
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

        <!-- Desktop nav links -->
        <nav class="hidden md:flex items-center gap-8" aria-label="Main navigation">
          <RouterLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="text-[length:var(--text-small)] font-medium uppercase tracking-[var(--tracking-label)] relative after:absolute after:bottom-0 after:left-0 after:h-px after:bg-current after:transition-[width] after:duration-[var(--duration-normal)] after:ease-[var(--ease-out-expo)] hover:after:w-full"
            :class="$route.path === link.to ? 'after:w-full' : 'after:w-0'"
          >
            {{ link.label }}
          </RouterLink>
        </nav>

        <!-- Right actions -->
        <div class="flex items-center gap-1">
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

          <!-- Hamburger (mobile only) -->
          <button
            class="md:hidden p-2 hover:opacity-70 transition-opacity duration-[var(--duration-fast)]"
            :aria-label="mobileMenuOpen ? 'Close menu' : 'Open menu'"
            :aria-expanded="mobileMenuOpen"
            @click="mobileMenuOpen = !mobileMenuOpen"
          >
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <Transition name="hamburger" mode="out-in">
                <g v-if="!mobileMenuOpen" key="open">
                  <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>
                </g>
                <g v-else key="close">
                  <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                </g>
              </Transition>
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile menu overlay -->
      <Transition name="mobile-menu">
        <nav
          v-if="mobileMenuOpen"
          class="md:hidden border-t border-[color:var(--color-border)] bg-[color:var(--color-surface)] px-[var(--spacing-container)] py-6 flex flex-col gap-5"
          aria-label="Mobile navigation"
        >
          <RouterLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="text-[length:var(--text-title)] font-light uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-on-surface)] hover:opacity-60 transition-opacity duration-[var(--duration-fast)]"
            :class="{ 'opacity-40': $route.path !== link.to }"
          >
            {{ link.label }}
          </RouterLink>
        </nav>
      </Transition>
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

  <!-- Cart Drawer -->
  <Teleport to="body">
    <CartDrawer :open="cartOpen" @close="cartOpen = false" />
  </Teleport>

  <!-- Toast notifications -->
  <ToastContainer />
</template>

<style>
.badge-pop-enter-active { transition: transform var(--duration-normal) var(--ease-out-expo); }
.badge-pop-enter-from { transform: scale(1.4); }
.badge-pop-enter-to { transform: scale(1); }

.mobile-menu-enter-active { transition: opacity var(--duration-normal) ease, transform var(--duration-normal) var(--ease-out-expo); }
.mobile-menu-leave-active { transition: opacity var(--duration-fast) ease, transform var(--duration-fast) ease; }
.mobile-menu-enter-from { opacity: 0; transform: translateY(-8px); }
.mobile-menu-leave-to  { opacity: 0; transform: translateY(-4px); }

.hamburger-enter-active, .hamburger-leave-active { transition: opacity var(--duration-fast) ease; }
.hamburger-enter-from, .hamburger-leave-to { opacity: 0; }
</style>
