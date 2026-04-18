<script setup lang="ts">
defineProps<{
  variant?: 'primary' | 'ghost' | 'danger'
  disabled?: boolean
  loading?: boolean
  size?: 'sm' | 'md'
}>()

defineEmits<{ click: [] }>()
</script>

<template>
  <button
    class="inline-flex items-center gap-1.5 font-medium uppercase tracking-wider rounded-lg transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed select-none"
    :class="[
      size === 'sm' ? 'px-3 py-1.5 text-[0.7rem]' : 'px-4 py-2 text-[0.75rem]',
      variant === 'ghost'  ? 'hover:opacity-80' : '',
      variant === 'danger' ? 'hover:opacity-80' : '',
      (!variant || variant === 'primary') ? 'hover:brightness-90' : '',
    ]"
    :style="
      variant === 'ghost'
        ? { border: '1.5px solid var(--admin-amber)', color: 'var(--admin-amber)', background: 'transparent' }
        : variant === 'danger'
        ? { border: '1.5px solid #F87171', color: '#B91C1C', background: 'transparent' }
        : { background: 'var(--admin-amber)', color: '#FFFFFF', border: 'none' }
    "
    :disabled="disabled || loading"
    @click="$emit('click')"
  >
    <span v-if="loading" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin flex-shrink-0" />
    <slot />
  </button>
</template>
