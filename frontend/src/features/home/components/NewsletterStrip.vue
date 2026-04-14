<script setup lang="ts">
import { ref } from 'vue'

const email = ref('')
const state = ref<'idle' | 'loading' | 'done'>('idle')

async function subscribe() {
  const val = email.value.trim()
  if (!val || !val.includes('@')) return
  state.value = 'loading'
  await new Promise(r => setTimeout(r, 600))
  state.value = 'done'
  email.value = ''
}
</script>

<template>
  <section class="bg-[color:var(--color-warm-beige-dk)] py-16 px-[var(--spacing-container)] border-y border-[color:var(--color-obsidian)]/6">
    <div class="max-w-[var(--container-max)] mx-auto flex flex-col md:flex-row md:items-center md:justify-between gap-8">

      <!-- Left copy -->
      <div class="shrink-0">
        <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] text-[color:var(--color-obsidian)]/35 mb-2">
          Acceso Exclusivo
        </p>
        <h2 class="text-[length:var(--text-title)] font-light uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-obsidian)]">
          Únete al círculo Vantier
        </h2>
        <p class="mt-2 text-[length:var(--text-micro)] text-[color:var(--color-obsidian)]/45">
          15% en tu primera compra · Acceso early a nuevas colecciones
        </p>
      </div>

      <!-- Right form -->
      <Transition name="swap" mode="out-in">
        <p
          v-if="state === 'done'"
          class="text-[length:var(--text-small)] text-[color:var(--color-amber-accent)] uppercase tracking-[var(--tracking-label)]"
        >
          Bienvenido al círculo.
        </p>
        <form
          v-else
          class="flex items-stretch w-full md:max-w-sm"
          @submit.prevent="subscribe"
        >
          <input
            v-model="email"
            type="email"
            placeholder="tu@email.com"
            class="flex-1 bg-transparent border-b border-[color:var(--color-obsidian)]/20 focus:border-[color:var(--color-obsidian)]/60 outline-none text-[length:var(--text-small)] text-[color:var(--color-obsidian)] placeholder-[color:var(--color-obsidian)]/25 pb-2 pr-4 uppercase tracking-[var(--tracking-label)] transition-colors duration-[var(--duration-normal)]"
          />
          <button
            type="submit"
            class="ml-3 w-10 h-10 flex items-center justify-center bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] hover:opacity-75 transition-opacity duration-[var(--duration-fast)] shrink-0"
            :aria-label="state === 'loading' ? 'Subscribing…' : 'Subscribe'"
          >
            <span v-if="state === 'loading'" class="w-3.5 h-3.5 border-2 border-current border-t-transparent rounded-full animate-spin" />
            <svg v-else class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </form>
      </Transition>
    </div>
  </section>
</template>

<style scoped>
.swap-enter-active { transition: opacity var(--duration-normal) ease; }
.swap-leave-active { transition: opacity var(--duration-fast) ease; }
.swap-enter-from, .swap-leave-to { opacity: 0; }
</style>
