<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useOrdersStore } from '../store'
import type { Order } from '../types'
import OrderCard from './OrderCard.vue'
import OrderDetailModal from './OrderDetailModal.vue'
import SeoHead from '@shared/components/SeoHead.vue'

const store = useOrdersStore()
const selectedOrder = ref<Order | null>(null)
const loading = ref(true)

onMounted(async () => {
  // TODO: replace with real API call — GET /api/orders
  await new Promise((r) => setTimeout(r, 500))
  store.orders = [
    {
      id: 'ord-00000001',
      status: 'delivered',
      items: [
        { productId: 'p1', variantId: 'v1', name: 'Polo Atelier — Classic', size: 'M', color: 'Ivory', priceUSD: 180, quantity: 2 },
      ],
      totalUSD: 360,
      shippingUSD: 0,
      discountUSD: 0,
      createdAt: '2026-03-01T00:00:00Z',
      trackingNumber: 'FX1234567890',
    },
  ]
  loading.value = false
})
</script>

<template>
  <SeoHead
    title="Your Orders — Vantier"
    description="View your Vantier order history"
    :robots="{ index: false, follow: false }"
  />

  <div class="max-w-3xl mx-auto px-[var(--spacing-container)] py-12">
    <h1 class="text-[length:var(--text-headline)] font-semibold mb-8 text-[color:var(--color-on-surface)] tracking-[var(--tracking-headline)]">
      Your Orders
    </h1>

    <div v-if="loading" class="space-y-3">
      <div v-for="i in 3" :key="i" class="h-20 bg-[color:var(--color-warm-beige)] animate-pulse" />
    </div>

    <div v-else-if="store.orders.length === 0" class="text-center py-16">
      <p class="text-[length:var(--text-small)] text-[color:var(--color-border-strong)]">No orders yet.</p>
    </div>

    <div v-else class="space-y-3">
      <OrderCard
        v-for="order in store.orders"
        :key="order.id"
        :order="order"
        @view="selectedOrder = $event"
      />
    </div>
  </div>

  <OrderDetailModal :order="selectedOrder" @close="selectedOrder = null" />
</template>
