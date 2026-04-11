<script setup lang="ts">
defineProps<{ quote: string }>()
</script>
<template>
  <blockquote class="font-[family-name:var(--font-editorial)] italic text-[length:var(--text-small)] leading-[var(--leading-loose,1.8)] text-[color:var(--color-on-surface)] opacity-75">
    "{{ quote }}"
  </blockquote>
</template>
