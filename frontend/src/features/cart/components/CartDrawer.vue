<script setup lang="ts">
import { useCartStore } from '@features/cart/store'
import CartItem from './CartItem.vue'
import CartSummary from './CartSummary.vue'
import CartEmpty from './CartEmpty.vue'

const props = defineProps<{ open: boolean }>()
const emit = defineEmits<{ (e: 'close'): void }>()

const cart = useCartStore()
</script>

<template>
  <!-- Backdrop -->
  <Transition name="cart-backdrop">
    <div
      v-if="props.open"
      class="fixed inset-0 z-40 bg-[color:var(--color-obsidian)]/30 backdrop-blur-[2px]"
      @click="emit('close')"
    />
  </Transition>

  <!-- Drawer panel -->
  <Transition name="cart-drawer">
    <div
      v-if="props.open"
      class="fixed top-0 right-0 z-50 h-full w-full max-w-md bg-[color:var(--color-surface)] flex flex-col shadow-2xl"
      role="dialog"
      aria-label="Shopping cart"
      aria-modal="true"
    >
      <!-- Header -->
      <div class="flex items-center justify-between px-6 py-5 border-b border-[color:var(--color-border)]">
        <h2 class="text-[length:var(--text-small)] tracking-[var(--tracking-label)] uppercase font-medium text-[color:var(--color-on-surface)]">
          Cart
          <span v-if="cart.totalItems > 0" class="ml-2 text-[color:var(--color-border-strong)]">({{ cart.totalItems }})</span>
        </h2>
        <button
          class="w-8 h-8 flex items-center justify-center text-[color:var(--color-on-surface)] hover:opacity-60 transition-opacity duration-[var(--duration-fast)]"
          aria-label="Close cart"
          @click="emit('close')"
        >
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>

      <!-- Items -->
      <div class="flex-1 overflow-y-auto px-6">
        <CartEmpty v-if="cart.items.length === 0" />
        <TransitionGroup
          v-else
          name="cart-item"
          tag="div"
        >
          <CartItem
            v-for="item in cart.items"
            :key="item.variantId"
            :item="item"
          />
        </TransitionGroup>
      </div>

      <!-- Summary -->
      <div v-if="cart.items.length > 0" class="px-6 pb-8 pt-2">
        <CartSummary />
      </div>
    </div>
  </Transition>
</template>

<style scoped>
/* Drawer slide-in/out */
.cart-drawer-enter-active {
  transition: transform var(--duration-slow) var(--ease-out-expo);
}
.cart-drawer-leave-active {
  transition: transform 300ms var(--ease-in-out-sin);
}
.cart-drawer-enter-from,
.cart-drawer-leave-to {
  transform: translateX(100%);
}

/* Backdrop fade */
.cart-backdrop-enter-active {
  transition: opacity var(--duration-normal) ease;
}
.cart-backdrop-leave-active {
  transition: opacity var(--duration-normal) ease;
}
.cart-backdrop-enter-from,
.cart-backdrop-leave-to {
  opacity: 0;
}

/* Cart item enter (slide from right) */
.cart-item-enter-active {
  transition: opacity var(--duration-normal) ease, transform var(--duration-normal) var(--ease-out-expo);
}
/* Cart item leave (fade + collapse) */
.cart-item-leave-active {
  transition: opacity 200ms ease, max-height 200ms ease, padding 200ms ease;
  overflow: hidden;
  max-height: 200px;
}
.cart-item-enter-from {
  opacity: 0;
  transform: translateX(20px);
}
.cart-item-leave-to {
  opacity: 0;
  max-height: 0;
  padding-top: 0;
  padding-bottom: 0;
}
.cart-item-move {
  transition: transform var(--duration-normal) var(--ease-out-expo);
}

/* Threshold pulse keyframe for FreeShippingBar */
@keyframes threshold-pulse {
  0%   { transform: scaleX(1); opacity: 1; }
  40%  { transform: scaleX(1.04); opacity: 0.85; }
  100% { transform: scaleX(1); opacity: 1; }
}
</style>
