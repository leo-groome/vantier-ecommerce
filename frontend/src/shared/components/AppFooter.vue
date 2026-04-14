<script setup lang="ts">
import { ref } from 'vue'

const email = ref('')
const submitted = ref(false)

function subscribe() {
  if (!email.value.trim()) return
  submitted.value = true
  email.value = ''
}
</script>

<template>
  <footer class="bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)]">
    <!-- Gold top rule -->
    <div class="w-full h-px bg-[color:var(--color-amber-accent)]" />

    <!-- Main grid -->
    <div class="max-w-[var(--container-max)] mx-auto px-[var(--spacing-container)] py-16 grid grid-cols-1 md:grid-cols-3 gap-12 md:gap-8">

      <!-- Left: Brand -->
      <div class="flex flex-col gap-4">
        <p class="text-[length:var(--text-small)] font-bold uppercase tracking-[var(--tracking-display)]">Vantier</p>
        <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-40 leading-relaxed">
          Los Angeles — México
        </p>
        <p class="text-[length:var(--text-micro)] opacity-30 leading-relaxed max-w-[220px] mt-2">
          Silent luxury. Crafted for those who move with purpose.
        </p>
      </div>

      <!-- Center: Collection links -->
      <div class="flex flex-col gap-4">
        <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] opacity-40">The Collection</p>
        <nav class="flex flex-col gap-3" aria-label="Collection navigation">
          <RouterLink
            v-for="item in [
              { label: 'Polo Atelier', to: '/shop?line=polo-atelier' },
              { label: 'Signature', to: '/shop?line=signature' },
              { label: 'Essential', to: '/shop?line=essential' },
              { label: 'All Products', to: '/shop' },
            ]"
            :key="item.to"
            :to="item.to"
            class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-60 hover:opacity-100 transition-opacity duration-[var(--duration-fast)] w-fit"
          >
            {{ item.label }}
          </RouterLink>
        </nav>
      </div>

      <!-- Right: Newsletter + social -->
      <div class="flex flex-col gap-6">
        <div>
          <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] opacity-40 mb-4">Stay in the know</p>

          <Transition name="form-swap" mode="out-in">
            <p v-if="submitted" class="text-[length:var(--text-micro)] text-[color:var(--color-amber-accent)] uppercase tracking-[var(--tracking-label)]">
              You're on the list.
            </p>
            <form v-else class="flex items-center border-b border-[color:var(--color-ivory)]/20 pb-1 focus-within:border-[color:var(--color-amber-accent)] transition-colors duration-[var(--duration-normal)]" @submit.prevent="subscribe">
              <input
                v-model="email"
                type="email"
                placeholder="your@email.com"
                class="flex-1 bg-transparent text-[length:var(--text-micro)] placeholder-[color:var(--color-ivory)]/25 text-[color:var(--color-ivory)] outline-none uppercase tracking-[var(--tracking-label)]"
              />
              <button
                type="submit"
                class="ml-3 opacity-40 hover:opacity-100 transition-opacity duration-[var(--duration-fast)]"
                aria-label="Subscribe"
              >
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
            </form>
          </Transition>
        </div>

        <!-- Social -->
        <div class="flex items-center gap-3">
          <a
            href="https://instagram.com/vantierluxuryla"
            target="_blank"
            rel="noopener noreferrer"
            class="opacity-40 hover:opacity-100 transition-opacity duration-[var(--duration-fast)]"
            aria-label="Instagram"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="2" y="2" width="20" height="20" rx="5" ry="5"/>
              <circle cx="12" cy="12" r="4"/>
              <circle cx="17.5" cy="6.5" r="0.5" fill="currentColor"/>
            </svg>
          </a>
          <span class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-30">@vantierluxuryla</span>
        </div>
      </div>
    </div>

    <!-- Bottom bar -->
    <div class="border-t border-[color:var(--color-ivory)]/8">
      <div class="max-w-[var(--container-max)] mx-auto px-[var(--spacing-container)] py-5 flex flex-col sm:flex-row items-center justify-between gap-3">
        <p class="text-[length:var(--text-micro)] opacity-25 uppercase tracking-[var(--tracking-label)]">
          © 2025 Vantier LLC
        </p>
        <nav class="flex items-center gap-6" aria-label="Legal navigation">
          <RouterLink
            v-for="item in [
              { label: 'Privacy', to: '/privacy' },
              { label: 'Shipping', to: '/shipping' },
              { label: 'Exchange Policy', to: '/exchange' },
            ]"
            :key="item.to"
            :to="item.to"
            class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-25 hover:opacity-60 transition-opacity duration-[var(--duration-fast)]"
          >
            {{ item.label }}
          </RouterLink>
        </nav>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.form-swap-enter-active { transition: opacity var(--duration-normal) ease; }
.form-swap-leave-active { transition: opacity var(--duration-fast) ease; }
.form-swap-enter-from, .form-swap-leave-to { opacity: 0; }
</style>
