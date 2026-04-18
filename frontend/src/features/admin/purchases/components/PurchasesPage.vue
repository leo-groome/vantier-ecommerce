<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AdminButton from '@features/admin/components/shared/AdminButton.vue'
import StatusBadge from '@features/admin/components/shared/StatusBadge.vue'
import type { AdminStatus } from '@features/admin/components/shared/StatusBadge.vue'
import { useAdminPurchasesStore } from '../store'
import type { PurchaseOrder, POStatus } from '../types'

const store = useAdminPurchasesStore()
const expanded = ref<Set<string>>(new Set())
const advancingId = ref<string | null>(null)

function mapStatus(s: POStatus): AdminStatus {
  if (s === 'ordered') return 'pendiente'
  if (s === 'in_transit') return 'procesando'
  return 'recibida'
}

function nextStatus(s: POStatus): POStatus | null {
  if (s === 'ordered') return 'in_transit'
  if (s === 'in_transit') return 'received'
  return null
}

function nextStatusLabel(s: POStatus): string {
  if (s === 'ordered') return 'Marcar En Tránsito'
  if (s === 'in_transit') return 'Marcar Recibida'
  return ''
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('es-MX', { day: 'numeric', month: 'short', year: 'numeric' })
}

function toggle(id: string) {
  if (expanded.value.has(id)) expanded.value.delete(id)
  else expanded.value.add(id)
}

async function advance(po: PurchaseOrder) {
  const next = nextStatus(po.status)
  if (!next) return
  advancingId.value = po.id
  await store.advanceStatus(po.id, next)
  advancingId.value = null
}

onMounted(() => store.loadOrders())
</script>

<template>
  <div class="space-y-6">
    <!-- Error -->
    <div v-if="store.error" class="text-[0.82rem] text-red-600 px-1">{{ store.error }}</div>

    <!-- Skeleton -->
    <div v-if="store.loading" class="space-y-3">
      <div v-for="i in 3" :key="i" class="h-20 rounded-xl animate-pulse" style="background: rgba(0,0,0,0.06);" />
    </div>

    <!-- Empty -->
    <div v-else-if="!store.loading && store.orders.length === 0" class="py-12 text-center text-[0.85rem]" style="color: var(--admin-text-secondary);">
      Sin órdenes de compra.
    </div>

    <!-- PO list -->
    <div v-else class="space-y-3">
      <div
        v-for="po in store.orders"
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
            <p class="text-[0.82rem] font-mono font-medium" style="color: var(--admin-text-primary);">{{ po.reference_number }}</p>
            <p class="text-[0.75rem] mt-0.5" style="color: var(--admin-text-secondary);">{{ po.supplier_name }}</p>
          </div>
          <div class="flex items-center gap-6 flex-shrink-0">
            <div class="text-right hidden sm:block">
              <p class="text-[0.72rem]" style="color: var(--admin-text-secondary);">{{ po.items.length }} ítem{{ po.items.length !== 1 ? 's' : '' }}</p>
              <p class="text-[0.72rem]" style="color: var(--admin-text-secondary);">{{ formatDate(po.created_at) }}</p>
            </div>
            <p v-if="po.expected_arrival_date" class="text-[0.72rem] font-medium" style="color: var(--admin-amber);">
              ETA: {{ formatDate(po.expected_arrival_date) }}
            </p>
            <StatusBadge :status="mapStatus(po.status)" />
          </div>
        </button>

        <Transition name="po-expand">
          <div v-if="expanded.has(po.id)" class="border-t" style="border-color: var(--admin-border);">
            <div class="overflow-x-auto">
              <table class="w-full text-[0.78rem]">
                <thead>
                  <tr style="background: var(--admin-bg);">
                    <th class="px-6 py-2.5 text-left font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Variante ID</th>
                    <th class="px-6 py-2.5 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Pedido</th>
                    <th class="px-6 py-2.5 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Recibido</th>
                  </tr>
                </thead>
                <tbody class="divide-y" style="border-color: var(--admin-border);">
                  <tr v-for="item in po.items" :key="item.id">
                    <td class="px-6 py-3 font-mono text-[0.7rem]" style="color: var(--admin-text-secondary);">{{ item.variant_id.slice(0, 8) }}…</td>
                    <td class="px-6 py-3 text-right font-medium" style="color: var(--admin-text-primary);">{{ item.qty_ordered }}</td>
                    <td class="px-6 py-3 text-right" :style="{ color: item.qty_received > 0 ? 'var(--status-ok-text)' : 'var(--admin-text-secondary)' }">{{ item.qty_received }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Notes + advance -->
            <div class="px-6 py-4 flex items-center justify-between gap-4" style="border-top: 1px solid var(--admin-border);">
              <p v-if="po.notes" class="text-[0.75rem] italic" style="color: var(--admin-text-secondary);">{{ po.notes }}</p>
              <div v-else />
              <AdminButton
                v-if="nextStatus(po.status)"
                variant="primary"
                :loading="advancingId === po.id"
                @click.stop="advance(po)"
              >
                {{ nextStatusLabel(po.status) }}
              </AdminButton>
              <span v-else class="text-[0.72rem] font-semibold uppercase tracking-wider" style="color: var(--status-ok-text);">Completada</span>
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
