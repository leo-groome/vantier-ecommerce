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
  <div class="min-h-screen flex items-center justify-center bg-[color:var(--color-warm-beige)]">
    <div class="w-full max-w-sm space-y-8 px-6">
      <!-- Brand -->
      <div class="text-center space-y-1">
        <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] text-[color:var(--color-obsidian)] font-bold">
          Vantier
        </p>
        <h1 class="text-lg font-semibold text-[color:var(--color-on-surface)] tracking-tight">
          Sign in
        </h1>
      </div>

      <!-- Form -->
      <form class="space-y-4" @submit.prevent="submit">
        <div class="space-y-1">
          <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-on-surface-muted)]">
            Email
          </label>
          <input
            v-model="email"
            type="email"
            required
            autocomplete="email"
            class="w-full px-3 py-2.5 rounded-[var(--radius-md)] border border-[color:var(--color-border)] bg-white text-sm text-[color:var(--color-on-surface)] outline-none focus:border-[color:var(--color-obsidian)] transition-colors"
          />
        </div>

        <div class="space-y-1">
          <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-on-surface-muted)]">
            Password
          </label>
          <input
            v-model="password"
            type="password"
            required
            autocomplete="current-password"
            class="w-full px-3 py-2.5 rounded-[var(--radius-md)] border border-[color:var(--color-border)] bg-white text-sm text-[color:var(--color-on-surface)] outline-none focus:border-[color:var(--color-obsidian)] transition-colors"
          />
        </div>

        <p v-if="error" class="text-xs text-red-500">{{ error }}</p>

        <button
          type="submit"
          :disabled="loading"
          class="w-full py-2.5 rounded-[var(--radius-md)] bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] font-semibold transition-opacity hover:opacity-90 disabled:opacity-50"
        >
          {{ loading ? 'Signing in…' : 'Sign in' }}
        </button>
      </form>
    </div>
  </div>
</template>
