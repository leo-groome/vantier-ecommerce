<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ margin: number }>()

const color = computed(() => {
  if (props.margin > 60) return '#2D7A4F'
  if (props.margin >= 40) return 'var(--admin-amber)'
  return '#B91C1C'
})

const showAlert = computed(() => props.margin < 50)
</script>

<template>
  <div class="space-y-1.5">
    <div class="h-1.5 rounded-full overflow-hidden" style="background: rgba(0,0,0,0.08);">
      <div
        class="h-full rounded-full transition-[width] duration-[600ms] ease-out"
        :style="{ width: Math.min(100, props.margin) + '%', background: color }"
      />
    </div>
    <p
      v-if="showAlert"
      class="inline-flex items-center gap-1 text-[0.62rem] font-medium px-2 py-0.5 rounded-full"
      style="background: var(--status-crit-bg); color: var(--status-crit-text);"
    >
      ⚠ Margen bajo
    </p>
  </div>
</template>
