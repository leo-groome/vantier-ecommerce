<script setup lang="ts">
import { RouterLink } from 'vue-router'

defineProps<{
  orderId: string
  email?: string
}>()
</script>

<template>
  <div class="max-w-lg mx-auto py-16 px-6 text-center space-y-6">
    <!-- Check icon -->
    <div class="w-12 h-12 mx-auto rounded-full bg-[color:var(--color-obsidian)] flex items-center justify-center">
      <svg class="w-6 h-6 text-[color:var(--color-ivory)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <polyline points="20 6 9 17 4 12" />
      </svg>
    </div>

    <div class="space-y-2">
      <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-border-strong)]">
        Order Confirmed
      </p>
      <h1 class="text-[length:var(--text-headline)] font-semibold text-[color:var(--color-on-surface)]">
        Thank you
      </h1>
      <p class="text-[length:var(--text-small)] text-[color:var(--color-border-strong)]">
        Order #{{ orderId }}
      </p>
    </div>

    <div class="border border-[color:var(--color-border)] p-5 text-left space-y-2">
      <p class="text-[length:var(--text-small)] text-[color:var(--color-on-surface)]">
        Estimated delivery: <span class="font-medium">5–7 business days</span>
      </p>
      <p v-if="email" class="text-[length:var(--text-small)] text-[color:var(--color-border-strong)]">
        Confirmation sent to {{ email }}
      </p>
      <p class="text-[length:var(--text-small)] text-[color:var(--color-border-strong)]">
        For exchanges, reply to your confirmation email or visit your account.
      </p>
    </div>

    <RouterLink
      to="/shop"
      class="inline-block px-10 py-3 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-[length:var(--text-small)] tracking-[var(--tracking-label)] uppercase hover:opacity-80 transition-opacity duration-[var(--duration-normal)]"
    >
      Continue Shopping
    </RouterLink>
  </div>
</template>
