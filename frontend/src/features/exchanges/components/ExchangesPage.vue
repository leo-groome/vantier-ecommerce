<script setup lang="ts">
import { onMounted } from 'vue'
import { useExchangesStore } from '../store'
import ExchangeStatusBadge from './ExchangeStatusBadge.vue'
import SeoHead from '@shared/components/SeoHead.vue'

const store = useExchangesStore()

function formatDate(iso: string) {
  return new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric' }).format(new Date(iso))
}

onMounted(async () => {
  // TODO: GET /api/exchanges
})
</script>

<template>
  <SeoHead
    title="Your Exchanges — Vantier"
    description="Track your exchange requests"
    :robots="{ index: false, follow: false }"
  />

  <div class="max-w-3xl mx-auto px-[var(--spacing-container)] py-12">
    <h1 class="text-[length:var(--text-headline)] font-semibold mb-8 text-[color:var(--color-on-surface)] tracking-[var(--tracking-headline)]">
      Exchanges
    </h1>

    <div v-if="store.exchanges.length === 0" class="text-center py-16">
      <p class="text-[length:var(--text-small)] text-[color:var(--color-border-strong)]">No exchange requests.</p>
    </div>

    <div v-else class="space-y-3">
      <div
        v-for="ex in store.exchanges"
        :key="ex.id"
        class="flex items-center justify-between p-5 border border-[color:var(--color-border)]"
      >
        <div class="space-y-1">
          <p class="text-[length:var(--text-small)] font-medium text-[color:var(--color-on-surface)]">
            Exchange #{{ ex.id.slice(-6).toUpperCase() }}
          </p>
          <p class="text-[length:var(--text-micro)] text-[color:var(--color-border-strong)]">
            Order #{{ ex.originalOrderId.slice(-8).toUpperCase() }} · {{ formatDate(ex.createdAt) }}
          </p>
        </div>
        <ExchangeStatusBadge :status="ex.status" />
      </div>
    </div>
  </div>
</template>
