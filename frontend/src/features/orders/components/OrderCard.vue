<script setup lang="ts">
import type { Order } from '../types'
import OrderStatusBadge from './OrderStatusBadge.vue'

defineProps<{ order: Order }>()
const emit = defineEmits<{ (e: 'view', order: Order): void }>()

function formatPrice(n: number) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n)
}
function formatDate(iso: string) {
  return new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric' }).format(new Date(iso))
}
</script>

<template>
  <div
    class="flex items-center justify-between p-5 border border-[color:var(--color-border)] hover:border-[color:var(--color-border-strong)] transition-colors duration-[var(--duration-fast)] cursor-pointer"
    @click="emit('view', order)"
  >
    <div class="space-y-1">
      <p class="text-[length:var(--text-small)] font-medium text-[color:var(--color-on-surface)]">
        Order #{{ order.id.slice(-8).toUpperCase() }}
      </p>
      <p class="text-[length:var(--text-micro)] text-[color:var(--color-border-strong)]">
        {{ formatDate(order.createdAt) }} · {{ order.items.length }} item{{ order.items.length !== 1 ? 's' : '' }}
      </p>
    </div>
    <div class="flex items-center gap-4">
      <OrderStatusBadge :status="order.status" />
      <p class="text-[length:var(--text-small)] font-medium text-[color:var(--color-on-surface)]">
        {{ formatPrice(order.totalUSD) }}
      </p>
      <svg class="w-4 h-4 text-[color:var(--color-border-strong)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <polyline points="9 18 15 12 9 6" />
      </svg>
    </div>
  </div>
</template>
