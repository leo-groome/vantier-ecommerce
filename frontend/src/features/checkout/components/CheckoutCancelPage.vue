<script setup lang="ts">
import { RouterLink } from 'vue-router'
import SeoHead from '@shared/components/SeoHead.vue'
</script>

<template>
  <SeoHead
    title="Payment Cancelled — Vantier"
    description="Your payment was cancelled."
    :robots="{ index: false, follow: false }"
  />
  <div class="max-w-lg mx-auto py-16 px-6 text-center space-y-6">
    <div class="w-12 h-12 mx-auto rounded-full border-2 border-[color:var(--color-border-strong)] flex items-center justify-center">
      <svg class="w-5 h-5 text-[color:var(--color-border-strong)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <line x1="18" y1="6" x2="6" y2="18" />
        <line x1="6" y1="6" x2="18" y2="18" />
      </svg>
    </div>

    <div class="space-y-2">
      <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-border-strong)]">
        Payment Cancelled
      </p>
      <h1 class="text-[length:var(--text-headline)] font-semibold text-[color:var(--color-on-surface)]">
        No charge was made
      </h1>
      <p class="text-[length:var(--text-small)] text-[color:var(--color-border-strong)]">
        Your cart is still saved. You can return and try again whenever you're ready.
      </p>
    </div>

    <RouterLink
      to="/checkout"
      class="inline-block px-10 py-3 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-[length:var(--text-small)] tracking-[var(--tracking-label)] uppercase hover:opacity-80 transition-opacity duration-[var(--duration-normal)]"
    >
      Return to Checkout
    </RouterLink>
  </div>
</template>
