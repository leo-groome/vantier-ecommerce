<script setup lang="ts">
defineProps<{
  label: string
  value: string
  sub?: string
  delta?: string
  deltaUp?: boolean
  icon: string
  valueColor?: string
}>()
</script>

<template>
  <div
    class="bg-white rounded-xl p-5 flex flex-col gap-3 transition-transform duration-150 hover:scale-[1.01]"
    style="box-shadow: var(--admin-card-shadow);"
  >
    <div class="flex items-start justify-between gap-2">
      <p
        class="text-[0.62rem] font-semibold uppercase tracking-wider leading-tight"
        style="color: var(--admin-text-secondary);"
      >{{ label }}</p>
      <svg
        class="w-5 h-5 flex-shrink-0 mt-0.5"
        style="color: var(--admin-amber);"
        viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"
      >
        <path :d="icon" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    <div class="flex items-end justify-between gap-2">
      <div>
        <p
          class="text-[2rem] font-bold leading-none tabular-nums"
          :style="{ color: valueColor ?? 'var(--admin-text-primary)' }"
        >{{ value }}</p>
        <p v-if="sub" class="mt-1 text-[0.72rem]" style="color: var(--admin-text-secondary);">{{ sub }}</p>
      </div>
      <span
        v-if="delta"
        class="text-[0.65rem] font-semibold px-2 py-0.5 rounded-full flex-shrink-0 mb-0.5"
        :style="deltaUp
          ? { background: 'var(--status-ok-bg)', color: 'var(--status-ok-text)' }
          : { background: 'var(--status-crit-bg)', color: 'var(--status-crit-text)' }"
      >{{ delta }}</span>
    </div>
  </div>
</template>
