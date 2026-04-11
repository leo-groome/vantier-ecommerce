<script setup lang="ts">
const props = defineProps<{
  size: string
  selected?: boolean
  available?: boolean
}>()
const emit = defineEmits<{ select: [] }>()
</script>
<template>
  <button
    type="button"
    :disabled="!available"
    @click="available && emit('select')"
    class="px-3 py-1.5 text-[length:var(--text-small)] font-medium border transition-colors duration-[var(--duration-fast)] focus-visible:outline-2 focus-visible:outline-offset-2"
    :class="[
      available ? 'cursor-pointer' : 'cursor-not-allowed opacity-35 line-through',
      selected
        ? 'bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] border-[color:var(--color-obsidian)]'
        : available
          ? 'bg-transparent text-[color:var(--color-on-surface)] border-[color:var(--color-border)] hover:border-[color:var(--color-border-strong)]'
          : 'bg-transparent text-[color:var(--color-on-surface)] border-[color:var(--color-border)]'
    ]"
  >
    {{ size }}
  </button>
</template>
