<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="flex flex-col items-center justify-center py-16 px-8 text-center">
    <div class="w-12 h-12 mb-6 text-[color:var(--color-border-strong)]">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" class="w-full h-full">
        <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z" />
        <line x1="3" y1="6" x2="21" y2="6" />
        <path d="M16 10a4 4 0 01-8 0" />
      </svg>
    </div>
    <p class="text-[length:var(--text-small)] tracking-[var(--tracking-label)] uppercase text-[color:var(--color-on-surface)] mb-2">
      Your cart is empty
    </p>
    <p class="text-[length:var(--text-small)] text-[color:var(--color-border-strong)] mb-8">
      Discover our curated collection
    </p>
    <RouterLink
      to="/shop"
      class="px-8 py-3 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-[length:var(--text-small)] tracking-[var(--tracking-label)] uppercase hover:opacity-80 transition-opacity duration-[var(--duration-normal)]"
    >
      Shop the Collection
    </RouterLink>
  </div>
</template>
