<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useCartStore } from '@features/cart/store'
import FreeShippingBar from '@shared/components/FreeShippingBar.vue'
import DiscountCodeInput from './DiscountCodeInput.vue'

const cart = useCartStore()

function formatPrice(n: number) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n)
}
</script>

<template>
  <div class="border-t border-[color:var(--color-border)] pt-4 space-y-4">
    <FreeShippingBar />

    <DiscountCodeInput />

    <div class="space-y-2 pt-2">
      <div class="flex justify-between text-[length:var(--text-small)] text-[color:var(--color-on-surface)]">
        <span>Subtotal</span>
        <span class="font-medium">{{ formatPrice(cart.subtotal) }}</span>
      </div>
      <div class="flex justify-between text-[length:var(--text-small)] text-[color:var(--color-border-strong)]">
        <span>Shipping</span>
        <span>{{ cart.freeShipping ? 'Free' : 'Calculated at checkout' }}</span>
      </div>
    </div>

    <RouterLink
      to="/checkout"
      class="block w-full text-center py-4 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-[length:var(--text-small)] tracking-[var(--tracking-label)] uppercase hover:opacity-80 transition-opacity duration-[var(--duration-normal)]"
    >
      Proceed to Checkout
    </RouterLink>

    <p class="text-center text-[length:var(--text-micro)] text-[color:var(--color-border-strong)]">
      Taxes calculated at checkout
    </p>
  </div>
</template>
