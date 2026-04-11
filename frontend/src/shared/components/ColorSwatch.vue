<script setup lang="ts">
const props = defineProps<{
  color: string       // CSS color value or named color
  label: string       // accessible label
  selected?: boolean
  disabled?: boolean
}>()
const emit = defineEmits<{ select: [] }>()
</script>
<template>
  <button
    type="button"
    :aria-label="label"
    :aria-pressed="selected"
    :disabled="disabled"
    @click="!disabled && emit('select')"
    class="relative w-6 h-6 rounded-full transition-all duration-[var(--duration-fast)] focus-visible:outline-2 focus-visible:outline-offset-2"
    :class="{
      'ring-2 ring-offset-2 ring-[color:var(--color-obsidian)]': selected,
      'opacity-30 cursor-not-allowed': disabled,
      'hover:scale-110 cursor-pointer': !disabled
    }"
    :style="{ backgroundColor: color }"
  >
    <span v-if="disabled" class="absolute inset-0 flex items-center justify-center">
      <span class="block w-[1px] h-full bg-white/60 rotate-45 absolute" />
    </span>
  </button>
</template>
