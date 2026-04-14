<script setup lang="ts">
import ProductFiltersPanel from './ProductFilters.vue'
import type { ProductFilters } from '../types'

const props = defineProps<{ open: boolean; modelValue: ProductFilters }>()
const emit = defineEmits<{
  (e: 'update:modelValue', val: ProductFilters): void
  (e: 'close'): void
}>()
</script>

<template>
  <!-- Backdrop -->
  <Transition name="filter-backdrop">
    <div
      v-if="props.open"
      class="fixed inset-0 z-40 bg-[color:var(--color-obsidian)]/40 backdrop-blur-[2px]"
      @click="emit('close')"
    />
  </Transition>

  <!-- Bottom-sheet panel -->
  <Transition name="filter-drawer">
    <div
      v-if="props.open"
      class="fixed bottom-0 left-0 right-0 z-50 bg-[color:var(--color-surface)] rounded-t-[1rem] shadow-2xl max-h-[80vh] flex flex-col"
      role="dialog"
      aria-label="Product filters"
      aria-modal="true"
    >
      <!-- Handle bar -->
      <div class="flex justify-center pt-3 pb-1 shrink-0">
        <div class="w-10 h-1 rounded-full bg-[color:var(--color-border)]" />
      </div>

      <!-- Header -->
      <div class="flex items-center justify-between px-6 py-4 border-b border-[color:var(--color-border)] shrink-0">
        <h2 class="text-[length:var(--text-small)] font-medium uppercase tracking-[var(--tracking-label)]">
          Filter
        </h2>
        <button
          class="w-8 h-8 flex items-center justify-center opacity-50 hover:opacity-100 transition-opacity duration-[var(--duration-fast)]"
          aria-label="Close filters"
          @click="emit('close')"
        >
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>

      <!-- Scrollable filter content -->
      <div class="flex-1 overflow-y-auto px-6 py-5">
        <ProductFiltersPanel
          :model-value="props.modelValue"
          @update:model-value="emit('update:modelValue', $event)"
        />
      </div>

      <!-- Apply button -->
      <div class="shrink-0 px-6 py-5 border-t border-[color:var(--color-border)]">
        <button
          class="w-full py-3.5 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-[length:var(--text-small)] font-medium uppercase tracking-[var(--tracking-label)] hover:opacity-80 transition-opacity duration-[var(--duration-fast)]"
          @click="emit('close')"
        >
          Apply Filters
        </button>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.filter-backdrop-enter-active { transition: opacity var(--duration-normal) ease; }
.filter-backdrop-leave-active { transition: opacity var(--duration-fast) ease; }
.filter-backdrop-enter-from, .filter-backdrop-leave-to { opacity: 0; }

.filter-drawer-enter-active { transition: transform var(--duration-normal) var(--ease-out-expo); }
.filter-drawer-leave-active { transition: transform var(--duration-fast) ease-in; }
.filter-drawer-enter-from { transform: translateY(100%); }
.filter-drawer-leave-to  { transform: translateY(100%); }
</style>
