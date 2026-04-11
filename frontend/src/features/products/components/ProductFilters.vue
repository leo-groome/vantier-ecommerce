<script setup lang="ts">
import { computed } from 'vue'
import type { ProductFilters } from '../types'

const props = defineProps<{ modelValue: ProductFilters }>()
const emit = defineEmits<{ 'update:modelValue': [ProductFilters] }>()

const lines = ['Polo Atelier', 'Signature', 'Essential'] as const
const styles = ['Classic', 'Design'] as const
const sizes = ['S', 'M', 'L', 'XL', 'XXL', 'XXXL']

function toggle(key: keyof ProductFilters, value: string) {
  const current = props.modelValue[key]
  emit('update:modelValue', {
    ...props.modelValue,
    [key]: current === value ? undefined : value,
  })
}
</script>
<template>
  <aside class="space-y-8">
    <!-- Line filter -->
    <div>
      <p class="text-[length:var(--text-micro)] font-medium uppercase tracking-[var(--tracking-label)] opacity-50 mb-3">Line</p>
      <div class="flex flex-col gap-2">
        <button
          v-for="line in lines"
          :key="line"
          @click="toggle('line', line)"
          class="text-left text-[length:var(--text-small)] uppercase tracking-[var(--tracking-label)] transition-opacity duration-[var(--duration-fast)]"
          :class="modelValue.line === line ? 'font-semibold opacity-100' : 'opacity-50 hover:opacity-80'"
        >
          {{ line }}
        </button>
      </div>
    </div>
    <!-- Style filter -->
    <div>
      <p class="text-[length:var(--text-micro)] font-medium uppercase tracking-[var(--tracking-label)] opacity-50 mb-3">Style</p>
      <div class="flex gap-2">
        <button
          v-for="style in styles"
          :key="style"
          @click="toggle('style', style)"
          class="px-3 py-1 text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] border transition-colors duration-[var(--duration-fast)]"
          :class="modelValue.style === style
            ? 'bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] border-[color:var(--color-obsidian)]'
            : 'border-[color:var(--color-border)] hover:border-[color:var(--color-border-strong)]'"
        >
          {{ style }}
        </button>
      </div>
    </div>
    <!-- Size filter -->
    <div>
      <p class="text-[length:var(--text-micro)] font-medium uppercase tracking-[var(--tracking-label)] opacity-50 mb-3">Size</p>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="size in sizes"
          :key="size"
          @click="toggle('size', size)"
          class="w-10 h-10 text-[length:var(--text-micro)] font-medium uppercase border transition-colors duration-[var(--duration-fast)]"
          :class="modelValue.size === size
            ? 'bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] border-[color:var(--color-obsidian)]'
            : 'border-[color:var(--color-border)] hover:border-[color:var(--color-border-strong)]'"
        >
          {{ size }}
        </button>
      </div>
    </div>
    <!-- Clear filters -->
    <button
      v-if="modelValue.line || modelValue.style || modelValue.size || modelValue.color"
      @click="emit('update:modelValue', {})"
      class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-40 hover:opacity-70 transition-opacity duration-[var(--duration-fast)]"
    >
      Clear filters
    </button>
  </aside>
</template>
