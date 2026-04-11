<script setup lang="ts">
import { ref } from 'vue'
import type { Order } from '../types'
import OrderStatusBadge from './OrderStatusBadge.vue'
import ExchangeRequestForm from '@features/exchanges/components/ExchangeRequestForm.vue'

const props = defineProps<{ order: Order | null }>()
const emit = defineEmits<{ (e: 'close'): void }>()

const showExchange = ref(false)
const exchangeTargetVariant = ref('')

function requestExchange(variantId: string) {
  exchangeTargetVariant.value = variantId
  showExchange.value = true
}

function onExchangeSubmit(data: { reason: string; preferredVariant: string }) {
  console.log('Exchange submitted', data)
  showExchange.value = false
  emit('close')
}

function formatPrice(n: number) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n)
}
function formatDate(iso: string) {
  return new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric' }).format(new Date(iso))
}
</script>

<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="order"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        @click.self="emit('close')"
      >
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-[color:var(--color-obsidian)]/40 backdrop-blur-[2px]" @click="emit('close')" />

        <!-- Panel -->
        <div class="relative z-10 bg-[color:var(--color-surface)] w-full max-w-lg max-h-[85vh] overflow-y-auto p-8 space-y-6">
          <div class="flex items-start justify-between">
            <div>
              <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-border-strong)]">
                {{ formatDate(order.createdAt) }}
              </p>
              <h2 class="text-[length:var(--text-title)] font-semibold mt-1">
                Order #{{ order.id.slice(-8).toUpperCase() }}
              </h2>
            </div>
            <div class="flex items-center gap-3">
              <OrderStatusBadge :status="order.status" />
              <button
                class="text-[color:var(--color-border-strong)] hover:text-[color:var(--color-obsidian)] transition-colors"
                aria-label="Close"
                @click="emit('close')"
              >
                <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Exchange form or item list -->
          <template v-if="showExchange">
            <ExchangeRequestForm
              :order-id="order.id"
              :variant-id="exchangeTargetVariant"
              @submit="onExchangeSubmit"
              @cancel="showExchange = false"
            />
          </template>
          <template v-else>
            <!-- Items -->
            <div class="divide-y divide-[color:var(--color-border)]">
              <div
                v-for="item in order.items"
                :key="item.variantId"
                class="flex justify-between items-start py-3 gap-4"
              >
                <div>
                  <p class="text-[length:var(--text-small)] text-[color:var(--color-on-surface)]">{{ item.name }}</p>
                  <p class="text-[length:var(--text-micro)] text-[color:var(--color-border-strong)]">{{ item.color }} · {{ item.size }} · qty {{ item.quantity }}</p>
                </div>
                <div class="flex items-center gap-3 flex-shrink-0">
                  <p class="text-[length:var(--text-small)]">{{ formatPrice(item.priceUSD * item.quantity) }}</p>
                  <button
                    v-if="order.status === 'delivered'"
                    class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] underline hover:opacity-70 transition-opacity"
                    @click="requestExchange(item.variantId)"
                  >
                    Exchange
                  </button>
                </div>
              </div>
            </div>

            <!-- Totals -->
            <div class="border-t border-[color:var(--color-border)] pt-4 space-y-1.5">
              <div class="flex justify-between text-[length:var(--text-small)] text-[color:var(--color-border-strong)]">
                <span>Shipping</span>
                <span>{{ order.shippingUSD === 0 ? 'Free' : formatPrice(order.shippingUSD) }}</span>
              </div>
              <div v-if="order.discountUSD > 0" class="flex justify-between text-[length:var(--text-small)] text-green-700">
                <span>Discount</span>
                <span>-{{ formatPrice(order.discountUSD) }}</span>
              </div>
              <div class="flex justify-between text-[length:var(--text-small)] font-semibold">
                <span>Total</span>
                <span>{{ formatPrice(order.totalUSD) }}</span>
              </div>
            </div>

            <p v-if="order.trackingNumber" class="text-[length:var(--text-small)] text-[color:var(--color-border-strong)]">
              Tracking: <span class="font-medium text-[color:var(--color-on-surface)]">{{ order.trackingNumber }}</span>
            </p>
          </template>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-enter-active, .modal-leave-active {
  transition: opacity var(--duration-normal) ease;
}
.modal-enter-from, .modal-leave-to {
  opacity: 0;
}
</style>
