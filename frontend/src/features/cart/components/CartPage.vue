<script setup lang="ts">
import { useCartStore } from '@features/cart/store'
import { useRouter } from 'vue-router'
import FreeShippingBar from '@shared/components/FreeShippingBar.vue'
import DiscountCodeInput from './DiscountCodeInput.vue'
import CartItem from './CartItem.vue'

const cart = useCartStore()
const router = useRouter()

function formatPrice(n: number) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n)
}
</script>

<template>
  <div class="max-w-[var(--container-max)] mx-auto px-[var(--spacing-container)] py-12">
    <div class="mb-8">
      <p class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)]">Your Selection</p>
      <h1 class="mt-1 text-[length:var(--text-headline)] font-semibold uppercase tracking-[var(--tracking-headline)]">Cart</h1>
    </div>

    <!-- Empty state -->
    <div v-if="cart.items.length === 0" class="flex flex-col items-center justify-center py-24 gap-6 text-center">
      <svg class="w-12 h-12 text-[color:var(--color-border)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
        <path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/>
      </svg>
      <div>
        <p class="text-[length:var(--text-title)] font-light uppercase tracking-[var(--tracking-headline)]">Your cart is empty</p>
        <p class="mt-2 text-[length:var(--text-small)] text-[color:var(--color-border-strong)]">Add items from the collection to get started.</p>
      </div>
      <RouterLink
        to="/shop"
        class="mt-2 px-8 py-3 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-[length:var(--text-small)] uppercase tracking-[var(--tracking-label)] hover:opacity-80 transition-opacity"
      >
        Shop the Collection
      </RouterLink>
    </div>

    <!-- Cart content -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-12">
      <!-- Items list -->
      <div class="lg:col-span-2">
        <TransitionGroup name="cart-item" tag="div">
          <CartItem
            v-for="item in cart.items"
            :key="item.variantId"
            :item="item"
          />
        </TransitionGroup>
      </div>

      <!-- Summary column -->
      <div class="lg:col-span-1">
        <div class="sticky top-24 space-y-6 border border-[color:var(--color-border)] p-6 bg-[color:var(--color-ivory)]">
          <p class="text-xs uppercase tracking-widest font-semibold text-[color:var(--color-obsidian)]">Order Summary</p>

          <FreeShippingBar />

          <DiscountCodeInput />

          <div class="space-y-2 pt-2 border-t border-[color:var(--color-border)]">
            <div class="flex justify-between text-[length:var(--text-small)]">
              <span>Subtotal</span>
              <span class="font-medium">{{ formatPrice(cart.subtotal) }}</span>
            </div>
            <div class="flex justify-between text-[length:var(--text-small)] text-[color:var(--color-border-strong)]">
              <span>Shipping</span>
              <span>{{ cart.freeShipping ? 'Free' : 'Calculated at checkout' }}</span>
            </div>
          </div>

          <button
            class="block w-full text-center py-4 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-[length:var(--text-small)] tracking-[var(--tracking-label)] uppercase hover:opacity-80 transition-opacity duration-[var(--duration-normal)]"
            @click="router.push('/checkout')"
          >
            Proceed to Checkout
          </button>

          <p class="text-center text-[length:var(--text-micro)] text-[color:var(--color-border-strong)]">
            Taxes calculated at checkout
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cart-item-enter-active { transition: opacity var(--duration-normal) ease, transform var(--duration-normal) var(--ease-out-expo); }
.cart-item-leave-active { transition: opacity 200ms ease, max-height 200ms ease; overflow: hidden; max-height: 200px; }
.cart-item-enter-from  { opacity: 0; transform: translateX(20px); }
.cart-item-leave-to    { opacity: 0; max-height: 0; }
.cart-item-move        { transition: transform var(--duration-normal) var(--ease-out-expo); }
</style>
