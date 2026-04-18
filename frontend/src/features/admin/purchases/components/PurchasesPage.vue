<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AdminButton from '@features/admin/components/shared/AdminButton.vue'
import StatusBadge from '@features/admin/components/shared/StatusBadge.vue'
import type { AdminStatus } from '@features/admin/components/shared/StatusBadge.vue'

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

function mapStatus(s: PurchaseOrder['status']): AdminStatus {
  if (s === 'draft') return 'pendiente'
  if (s === 'ordered') return 'confirmada'
  return 'recibida'
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
    <!-- Actions -->
    <div class="flex justify-end">
      <AdminButton variant="primary">
        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        Nueva Orden
      </AdminButton>
    </div>

    <!-- Skeleton -->
    <div v-if="loading" class="space-y-3">
      <div v-for="i in 3" :key="i" class="h-20 rounded-xl animate-pulse" style="background: rgba(0,0,0,0.06);" />
    </div>

    <!-- PO list -->
    <div v-else class="space-y-3">
      <div
        v-for="po in pos"
        :key="po.id"
        class="bg-white rounded-xl overflow-hidden border border-transparent transition-all duration-200"
        :style="{ boxShadow: 'var(--admin-card-shadow)', borderColor: expanded.has(po.id) ? 'var(--admin-amber)' : 'transparent' }"
      >
        <button
          class="w-full flex items-center gap-4 px-6 py-4 hover:bg-black/[0.02] transition-colors text-left"
          @click="toggle(po.id)"
        >
          <svg
            class="w-4 h-4 flex-shrink-0 transition-transform duration-200"
            :class="expanded.has(po.id) ? 'rotate-90' : ''"
            style="color: var(--admin-text-secondary);"
            viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
          >
            <polyline points="9 18 15 12 9 6"/>
          </svg>
          <div class="flex-1 min-w-0">
            <p class="text-[0.82rem] font-mono font-medium" style="color: var(--admin-text-primary);">{{ po.id }}</p>
            <p class="text-[0.75rem] mt-0.5" style="color: var(--admin-text-secondary);">{{ po.supplier }}</p>
          </div>
          <div class="flex items-center gap-6 flex-shrink-0">
            <div class="text-right hidden sm:block">
              <p class="text-[0.72rem]" style="color: var(--admin-text-secondary);">{{ po.items.length }} Items</p>
              <p class="text-[0.72rem]" style="color: var(--admin-text-secondary);">{{ po.date }}</p>
            </div>
            <p v-if="po.eta" class="text-[0.72rem] font-medium" style="color: var(--admin-amber);">ETA: {{ po.eta }}</p>
            <p class="text-[0.85rem] font-bold" style="color: var(--admin-text-primary);">${{ po.total.toLocaleString() }}</p>
            <StatusBadge :status="mapStatus(po.status)" />
          </div>
        </button>

        <Transition name="po-expand">
          <div v-if="expanded.has(po.id)" class="border-t" style="border-color: var(--admin-border);">
            <div class="overflow-x-auto">
              <table class="w-full text-[0.78rem]">
                <thead>
                  <tr style="background: var(--admin-bg);">
                    <th class="px-6 py-2.5 text-left font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">SKU</th>
                    <th class="px-6 py-2.5 text-left font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Item</th>
                    <th class="px-6 py-2.5 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Qty</th>
                    <th class="px-6 py-2.5 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Unit Cost</th>
                    <th class="px-6 py-2.5 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Subtotal</th>
                  </tr>
                </thead>
                <tbody class="divide-y" style="border-color: var(--admin-border);">
                  <tr v-for="item in po.items" :key="item.sku">
                    <td class="px-6 py-3 font-mono text-[0.7rem]" style="color: var(--admin-text-secondary);">{{ item.sku }}</td>
                    <td class="px-6 py-3" style="color: var(--admin-text-primary);">{{ item.name }}</td>
                    <td class="px-6 py-3 text-right" style="color: var(--admin-text-secondary);">{{ item.qty }}</td>
                    <td class="px-6 py-3 text-right" style="color: var(--admin-text-secondary);">${{ item.costUSD }}</td>
                    <td class="px-6 py-3 text-right font-medium" style="color: var(--admin-text-primary);">${{ (item.qty * item.costUSD).toLocaleString() }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </Transition>
      </div>
    </div>
  </div>
</template>

<style scoped>
.po-expand-enter-active { transition: max-height 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.2s ease; overflow: hidden; }
.po-expand-leave-active { transition: max-height 0.2s ease, opacity 0.1s ease; overflow: hidden; }
.po-expand-enter-from, .po-expand-leave-to { max-height: 0; opacity: 0; }
.po-expand-enter-to, .po-expand-leave-from { max-height: 1000px; opacity: 1; }
</style>
