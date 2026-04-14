<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface PurchaseOrder {
  id: string
  supplier: string
  items: { sku: string; name: string; qty: number; costUSD: number }[]
  status: 'draft' | 'ordered' | 'received'
  total: number
  date: string
  eta: string | null
}

const pos = ref<PurchaseOrder[]>([])
const loading = ref(true)

const STATUS_COLORS: Record<string, string> = {
  draft:    'text-[color:var(--color-border-strong)] bg-[color:var(--color-warm-beige)] border-[color:var(--color-border)]',
  ordered:  'text-blue-700 bg-blue-50 border-blue-200',
  received: 'text-emerald-700 bg-emerald-50 border-emerald-200',
}

const expanded = ref<Set<string>>(new Set())

function toggle(id: string) {
  if (expanded.value.has(id)) expanded.value.delete(id)
  else expanded.value.add(id)
}

onMounted(() => {
  setTimeout(() => {
    pos.value = [
      {
        id: 'PO-2024-001',
        supplier: 'Textiles Selectos SA',
        items: [
          { sku: 'PA-CL-IVY-L',  name: 'Polo Atelier Classic — Ivory L',     qty: 20, costUSD: 62 },
          { sku: 'PA-CL-OBS-L',  name: 'Polo Atelier Classic — Obsidian L',  qty: 20, costUSD: 62 },
          { sku: 'PA-CL-OBS-XL', name: 'Polo Atelier Classic — Obsidian XL', qty: 15, costUSD: 62 },
        ],
        status: 'received',
        total: 3410,
        date: 'Mar 15, 2024',
        eta: null,
      },
      {
        id: 'PO-2024-002',
        supplier: 'Textiles Selectos SA',
        items: [
          { sku: 'PA-DS-OBS-XL',  name: 'Polo Atelier Design — Obsidian XL',  qty: 25, costUSD: 68 },
          { sku: 'SIG-DS-MID-XL', name: 'Signature Shirt — Midnight XL',      qty: 20, costUSD: 75 },
        ],
        status: 'ordered',
        total: 3200,
        date: 'Apr 5, 2024',
        eta: 'Apr 18, 2024',
      },
      {
        id: 'PO-2024-003',
        supplier: 'Cotton & Co.',
        items: [
          { sku: 'ESS-CL-WB-L', name: 'Essential Tee — Warm Beige L', qty: 30, costUSD: 32 },
          { sku: 'ESS-CL-WB-XL', name: 'Essential Tee — Warm Beige XL', qty: 30, costUSD: 32 },
        ],
        status: 'draft',
        total: 1920,
        date: 'Apr 10, 2024',
        eta: null,
      },
    ]
    loading.value = false
  }, 400)
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-end justify-between gap-4">
      <div>
        <p class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)]">Procurement</p>
        <h1 class="mt-1 text-2xl font-semibold uppercase tracking-wider text-[color:var(--color-obsidian)]">Purchases</h1>
      </div>
      <button class="flex items-center gap-2 px-4 py-2.5 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-xs uppercase tracking-widest rounded-[var(--radius-md)] hover:opacity-80 transition-opacity duration-[var(--duration-fast)]">
        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        New PO
      </button>
    </div>

    <!-- Skeleton -->
    <div v-if="loading" class="space-y-3">
      <div v-for="i in 3" :key="i" class="h-16 rounded-[var(--radius-md)] bg-[color:var(--color-warm-beige-dk)] animate-pulse" />
    </div>

    <!-- PO list -->
    <div v-else class="space-y-2">
      <div
        v-for="po in pos"
        :key="po.id"
        class="bg-[color:var(--color-ivory)] border border-[color:var(--color-border)] rounded-[var(--radius-md)] overflow-hidden"
      >
        <button
          class="w-full flex items-center gap-4 px-5 py-4 hover:bg-[color:var(--color-warm-beige)] transition-colors duration-[var(--duration-fast)] text-left"
          @click="toggle(po.id)"
        >
          <svg
            class="w-4 h-4 flex-shrink-0 text-[color:var(--color-border-strong)] transition-transform duration-[var(--duration-normal)]"
            :class="expanded.has(po.id) ? 'rotate-90' : ''"
            viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
          >
            <polyline points="9 18 15 12 9 6"/>
          </svg>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-[color:var(--color-obsidian)] font-mono">{{ po.id }}</p>
            <p class="text-xs text-[color:var(--color-border-strong)] mt-0.5">{{ po.supplier }}</p>
          </div>
          <div class="flex items-center gap-6 flex-shrink-0">
            <div class="text-right">
              <p class="text-xs text-[color:var(--color-border-strong)]">{{ po.items.length }} SKUs</p>
              <p class="text-xs text-[color:var(--color-border-strong)]">{{ po.date }}</p>
            </div>
            <p v-if="po.eta" class="text-xs text-blue-600">ETA: {{ po.eta }}</p>
            <p class="text-sm font-semibold text-[color:var(--color-obsidian)]">${{ po.total.toLocaleString() }}</p>
            <span
              class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium uppercase tracking-wider border"
              :class="STATUS_COLORS[po.status]"
            >{{ po.status }}</span>
          </div>
        </button>

        <Transition name="po-expand">
          <div v-if="expanded.has(po.id)" class="border-t border-[color:var(--color-border)]">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-[color:var(--color-warm-beige)] text-xs uppercase tracking-widest text-[color:var(--color-border-strong)]">
                  <th class="px-5 py-2 text-left font-medium">SKU</th>
                  <th class="px-5 py-2 text-left font-medium">Item</th>
                  <th class="px-5 py-2 text-right font-medium">Qty</th>
                  <th class="px-5 py-2 text-right font-medium">Unit Cost</th>
                  <th class="px-5 py-2 text-right font-medium">Subtotal</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-[color:var(--color-border)]">
                <tr v-for="item in po.items" :key="item.sku">
                  <td class="px-5 py-3 font-mono text-xs text-[color:var(--color-border-strong)]">{{ item.sku }}</td>
                  <td class="px-5 py-3 text-[color:var(--color-obsidian)]">{{ item.name }}</td>
                  <td class="px-5 py-3 text-right text-[color:var(--color-border-strong)]">{{ item.qty }}</td>
                  <td class="px-5 py-3 text-right text-[color:var(--color-border-strong)]">${{ item.costUSD }}</td>
                  <td class="px-5 py-3 text-right font-medium text-[color:var(--color-obsidian)]">${{ (item.qty * item.costUSD).toLocaleString() }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </Transition>
      </div>
    </div>
  </div>
</template>

<style scoped>
.po-expand-enter-active { transition: max-height var(--duration-normal) var(--ease-out-expo), opacity var(--duration-normal) ease; overflow: hidden; }
.po-expand-leave-active { transition: max-height var(--duration-fast) ease, opacity var(--duration-fast) ease; overflow: hidden; }
.po-expand-enter-from, .po-expand-leave-to { max-height: 0; opacity: 0; }
.po-expand-enter-to, .po-expand-leave-from { max-height: 500px; opacity: 1; }
</style>
