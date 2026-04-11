<script setup lang="ts">
import { computed } from 'vue'
import { useCartStore } from '@features/cart/store'

const cart = useCartStore()
const THRESHOLD = 5
const progress = computed(() => Math.min(cart.totalItems / THRESHOLD, 1))
const remaining = computed(() => Math.max(THRESHOLD - cart.totalItems, 0))
const achieved = computed(() => cart.totalItems >= THRESHOLD)
</script>
<template>
  <div class="w-full">
    <p class="text-[length:var(--text-micro)] font-medium mb-2 text-[color:var(--color-on-surface)]">
      <span v-if="achieved">Free shipping applied</span>
      <span v-else>Add {{ remaining }} more item{{ remaining !== 1 ? 's' : '' }} for free shipping</span>
    </p>
    <div class="h-0.5 bg-[color:var(--color-border)] w-full overflow-hidden">
      <div
        class="h-full bg-[color:var(--color-amber-accent)] transition-[width] duration-[var(--duration-slow)] ease-[var(--ease-out-expo)]"
        :style="{ width: `${progress * 100}%` }"
        :class="{ 'animate-[threshold-pulse_400ms_ease-out_1]': achieved }"
      />
    </div>
  </div>
</template>
