<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  current: number
  threshold?: number
}>()

const max = computed(() => props.threshold ?? 50)
const pct = computed(() => Math.min(100, Math.max(0, (props.current / max.value) * 100)))

const color = computed(() => {
  if (pct.value > 30) return '#2D7A4F'
  if (pct.value >= 10) return 'var(--admin-amber)'
  return '#B91C1C'
})

const textColor = computed(() => {
  if (pct.value > 30) return '#2D7A4F'
  if (pct.value >= 10) return '#92600F'
  return '#B91C1C'
})
</script>

<template>
  <div class="flex items-center gap-2 min-w-0">
    <div class="w-14 h-1 rounded-full flex-shrink-0 overflow-hidden" style="background: rgba(0,0,0,0.08);">
      <div
        class="h-full rounded-full transition-[width] duration-[600ms] ease-out"
        :style="{ width: pct + '%', background: color }"
      />
    </div>
    <span
      class="text-[0.75rem] font-semibold flex-shrink-0 tabular-nums"
      :style="{ color: textColor }"
    >{{ current }}</span>
  </div>
</template>
