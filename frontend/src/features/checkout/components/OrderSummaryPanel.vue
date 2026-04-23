<script setup lang="ts">
import { computed } from 'vue'
import { useCartStore } from '@features/cart/store'
import type { ShippingRate } from '../types'

const props = defineProps<{ shippingRate?: ShippingRate | null }>()

const cart = useCartStore()
const total = computed(() => cart.subtotal + (props.shippingRate?.price_usd ?? 0))

function formatPrice(n: number) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n)
}
</script>

<template>
  <aside class="sticky top-24 bg-[color:var(--color-warm-beige)] p-6 space-y-4">
    <h2 class="text-[length:var(--text-small)] tracking-[var(--tracking-label)] uppercase font-medium">Order Summary</h2>

    <!-- Line items -->
    <div class="space-y-3 border-b border-[color:var(--color-border)] pb-4">
      <div
        v-for="item in cart.items"
        :key="item.variantId"
        class="flex justify-between gap-4"
      >
        <div class="flex-1 min-w-0">
          <p class="text-[length:var(--text-small)] truncate text-[color:var(--color-on-surface)]">{{ item.name }}</p>
          <p class="text-[length:var(--text-micro)] text-[color:var(--color-border-strong)]">{{ item.color }} · {{ item.size }} · qty {{ item.quantity }}</p>
        </div>
        <p class="text-[length:var(--text-small)] text-[color:var(--color-on-surface)] flex-shrink-0">
          {{ formatPrice(item.priceUSD * item.quantity) }}
        </p>
      </div>
    </div>

    <!-- Totals -->
    <div class="space-y-2">
      <div class="flex justify-between text-[length:var(--text-small)] text-[color:var(--color-on-surface)]">
        <span>Subtotal</span>
        <span>{{ formatPrice(cart.subtotal) }}</span>
      </div>
      <div class="flex justify-between text-[length:var(--text-small)] text-[color:var(--color-border-strong)]">
        <span>Shipping</span>
        <span>
          <span v-if="!shippingRate">—</span>
          <span v-else-if="cart.freeShipping || shippingRate.price_usd === 0">Free</span>
          <span v-else>{{ formatPrice(shippingRate.price_usd) }}</span>
        </span>
      </div>
      <div class="flex justify-between text-[length:var(--text-small)] font-semibold text-[color:var(--color-on-surface)] pt-2 border-t border-[color:var(--color-border)]">
        <span>Total</span>
        <span>{{ formatPrice(total) }}</span>
      </div>
    </div>
  </aside>
</template>
