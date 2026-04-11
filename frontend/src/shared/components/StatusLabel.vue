<script setup lang="ts">
defineProps<{ category: string; status: string }>()
</script>
<template>
  <p class="text-[length:var(--text-micro)] font-medium uppercase tracking-[var(--tracking-label)] text-[color:var(--color-on-surface)] opacity-50">
    {{ category }} — {{ status }}
  </p>
</template>
