<script setup lang="ts">
defineProps<{ stock: number; threshold?: number }>()
</script>
<template>
  <span
    v-if="stock <= (threshold ?? 50) && stock > 0"
    class="inline-block text-[length:var(--text-micro)] font-medium uppercase tracking-[var(--tracking-label)] text-[color:var(--color-amber-accent)] border border-[color:var(--color-amber-accent)] px-2 py-0.5"
  >
    Only {{ stock }} left
  </span>
</template>
