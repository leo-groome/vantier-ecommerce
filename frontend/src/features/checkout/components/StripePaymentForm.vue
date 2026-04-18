<script setup lang="ts">
defineProps<{
  loading?: boolean
  error?: string
}>()

const emit = defineEmits<{ (e: 'submit'): void }>()
</script>

<template>
  <div class="space-y-4">
    <p v-if="error" class="text-[length:var(--text-micro)] text-red-600">{{ error }}</p>

    <button
      :disabled="loading"
      class="w-full py-4 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-[length:var(--text-small)] tracking-[var(--tracking-label)] uppercase hover:opacity-80 disabled:opacity-40 transition-opacity duration-[var(--duration-normal)] flex items-center justify-center gap-3"
      @click="emit('submit')"
    >
      <span v-if="loading" class="w-4 h-4 border-2 border-[color:var(--color-ivory)] border-t-transparent rounded-full animate-spin" />
      <span>{{ loading ? 'Redirecting to payment…' : 'Pay with Stripe' }}</span>
    </button>

    <p class="text-center text-[length:var(--text-micro)] text-[color:var(--color-border-strong)]">
      Secured by Stripe · SSL encrypted
    </p>
  </div>
</template>
