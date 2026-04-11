<script setup lang="ts">
defineProps<{ text: string }>()
</script>
<template>
  <p class="text-[length:var(--text-micro)] font-medium uppercase tracking-[var(--tracking-label)] text-[color:var(--color-on-surface)] opacity-60">
    {{ text }}
  </p>
</template>
