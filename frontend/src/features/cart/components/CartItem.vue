<script setup lang="ts">
import { ref, watch } from 'vue'
import { useCartStore } from '@features/cart/store'
import type { CartItem } from '@features/cart/types'

const props = defineProps<{ item: CartItem }>()

const cart = useCartStore()
const qtyBump = ref(false)

function increment() {
  cart.addItem({ ...props.item, quantity: 1 })
}

function decrement() {
  if (props.item.quantity <= 1) {
    cart.removeItem(props.item.variantId)
  } else {
    const updated = { ...props.item, quantity: props.item.quantity - 1 }
    cart.removeItem(props.item.variantId)
    cart.addItem(updated)
  }
}

watch(
  () => props.item.quantity,
  () => {
    qtyBump.value = true
    setTimeout(() => (qtyBump.value = false), 150)
  }
)

function formatPrice(n: number) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n)
}
</script>

<template>
  <div class="flex gap-4 py-4 border-b border-[color:var(--color-border)] last:border-0">
    <!-- Image placeholder (real image via product store lookup, skipped for now) -->
    <div class="w-16 h-20 bg-[color:var(--color-warm-beige)] flex-shrink-0" />

    <div class="flex-1 min-w-0">
      <div class="flex justify-between items-start gap-2">
        <p class="text-[length:var(--text-small)] font-medium text-[color:var(--color-on-surface)] truncate">
          {{ item.name }}
        </p>
        <button
          class="text-[color:var(--color-border-strong)] hover:text-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)] flex-shrink-0"
          aria-label="Remove item"
          @click="cart.removeItem(item.variantId)"
        >
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>

      <p class="text-[length:var(--text-micro)] text-[color:var(--color-border-strong)] mt-0.5">
        {{ item.color }} · {{ item.size }}
      </p>

      <!-- Personalization Info -->
      <div v-if="item.isPersonalized" class="mt-2 text-[length:var(--text-micro)] text-[color:var(--color-amber-accent)] bg-[#0d0c0a] border border-[#2a2520] p-2 flex items-center gap-2">
        <div class="w-6 h-6 flex items-center justify-center bg-[color:var(--color-amber-accent)]/10 text-[color:var(--color-amber-accent)] flex-shrink-0">
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
        </div>
        <div>
          <span class="uppercase tracking-[var(--tracking-label)] opacity-80 block text-[9px]">Custom Design</span>
          <span class="text-[color:var(--color-ivory)] opacity-90">{{ item.customizationPlacement }}</span>
        </div>
      </div>

      <div class="flex items-center justify-between mt-3">
        <!-- Qty stepper -->
        <div class="flex items-center border border-[color:var(--color-border)]">
          <button
            class="w-7 h-7 flex items-center justify-center text-[color:var(--color-on-surface)] hover:bg-[color:var(--color-warm-beige)] transition-colors duration-[var(--duration-fast)]"
            aria-label="Decrease quantity"
            @click="decrement"
          >
            <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12" /></svg>
          </button>
          <span
            class="w-8 text-center text-[length:var(--text-small)] transition-transform duration-[var(--duration-fast)]"
            :class="{ 'scale-[1.2]': qtyBump }"
          >
            {{ item.quantity }}
          </span>
          <button
            class="w-7 h-7 flex items-center justify-center text-[color:var(--color-on-surface)] hover:bg-[color:var(--color-warm-beige)] transition-colors duration-[var(--duration-fast)]"
            aria-label="Increase quantity"
            @click="increment"
          >
            <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" /></svg>
          </button>
        </div>

        <p class="text-[length:var(--text-small)] font-medium text-[color:var(--color-on-surface)]">
          {{ formatPrice(item.priceUSD * item.quantity) }}
        </p>
      </div>
    </div>
  </div>
</template>
