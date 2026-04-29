<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../store'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const email = ref('')
const password = ref('')
const error = ref<string | null>(null)
const loading = ref(false)

async function submit() {
  error.value = null
  loading.value = true
  try {
    await auth.login(email.value, password.value)
    const redirect = (route.query.redirect as string) ?? (auth.isAdmin ? '/admin/dashboard' : '/')
    await router.push(redirect)
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Login failed. Check your credentials.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="space-y-8">
    <!-- Heading -->
    <div class="space-y-1">
      <h1
        class="text-[1.6rem] font-bold tracking-tight"
        style="color: var(--color-obsidian);"
      >
        Iniciar sesión
      </h1>
      <p
        class="text-[0.82rem]"
        style="color: rgba(0,0,0,0.4);"
      >
        Ingresa tus credenciales para acceder al panel.
      </p>
    </div>

    <!-- Form -->
    <form class="space-y-5" @submit.prevent="submit">
      <div class="space-y-1.5">
        <label
          class="block text-[0.68rem] font-semibold uppercase tracking-wider"
          style="color: var(--color-obsidian);"
        >
          Correo electrónico
        </label>
        <input
          v-model="email"
          type="email"
          required
          autocomplete="email"
          placeholder="admin@vantierluxuryla.com"
          class="w-full px-4 py-3 rounded-xl border text-[0.88rem] outline-none transition-all"
          style="border-color: rgba(0,0,0,0.12); background: #fff; color: var(--color-obsidian);"
          :style="{ boxShadow: 'none' }"
          @focus="($event.target as HTMLInputElement).style.borderColor = 'var(--color-obsidian)'"
          @blur="($event.target as HTMLInputElement).style.borderColor = 'rgba(0,0,0,0.12)'"
        />
      </div>

      <div class="space-y-1.5">
        <label
          class="block text-[0.68rem] font-semibold uppercase tracking-wider"
          style="color: var(--color-obsidian);"
        >
          Contraseña
        </label>
        <input
          v-model="password"
          type="password"
          required
          autocomplete="current-password"
          placeholder="••••••••"
          class="w-full px-4 py-3 rounded-xl border text-[0.88rem] outline-none transition-all"
          style="border-color: rgba(0,0,0,0.12); background: #fff; color: var(--color-obsidian);"
          @focus="($event.target as HTMLInputElement).style.borderColor = 'var(--color-obsidian)'"
          @blur="($event.target as HTMLInputElement).style.borderColor = 'rgba(0,0,0,0.12)'"
        />
      </div>

      <p v-if="error" class="text-[0.78rem] text-red-500 flex items-center gap-1.5">
        <svg class="w-3.5 h-3.5 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        {{ error }}
      </p>

      <button
        type="submit"
        :disabled="loading"
        class="w-full py-3 rounded-xl text-[0.75rem] font-bold uppercase tracking-widest transition-all disabled:opacity-50"
        style="background: var(--color-obsidian); color: #fff;"
      >
        <span v-if="loading" class="inline-flex items-center gap-2">
          <span class="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          Ingresando…
        </span>
        <span v-else>Ingresar</span>
      </button>
    </form>
  </div>
</template>
