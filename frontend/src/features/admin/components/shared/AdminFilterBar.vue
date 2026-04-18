<script setup lang="ts">
defineProps<{
  modelValue: string
  placeholder?: string
}>()

defineEmits<{ 'update:modelValue': [string] }>()
</script>

<template>
  <div class="flex items-center gap-2 flex-wrap">
    <!-- Search -->
    <div class="relative">
      <svg
        class="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 pointer-events-none"
        style="color: var(--admin-text-secondary);"
        viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
      >
        <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35" stroke-linecap="round"/>
      </svg>
      <input
        :value="modelValue"
        :placeholder="placeholder ?? 'Buscar…'"
        type="text"
        class="pl-9 pr-3 py-1.5 text-[0.78rem] rounded-lg bg-white focus:outline-none transition-shadow"
        style="border: 1.5px solid rgba(0,0,0,0.1); color: var(--admin-text-primary); min-width: 220px;"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      />
    </div>
    <!-- Extra controls via slot (selects, pills…) -->
    <slot />
  </div>
</template>
