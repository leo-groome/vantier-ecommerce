<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminStatCard from '@features/admin/components/shared/AdminStatCard.vue'
import StatusBadge from '@features/admin/components/shared/StatusBadge.vue'
import AdminButton from '@features/admin/components/shared/AdminButton.vue'
import AdminFilterBar from '@features/admin/components/shared/AdminFilterBar.vue'
import type { AdminStatus } from '@features/admin/components/shared/StatusBadge.vue'
import { useAdminOrdersStore } from '../store'
import type { AdminOrder, OrderStatus } from '../types'

const store = useAdminOrdersStore()

const STATUS_MAP: Record<OrderStatus, AdminStatus> = {
  pending:    'pendiente',
  processing: 'procesando',
  shipped:    'enviado',
  delivered:  'entregado',
  cancelled:  'inactivo',
}

const search         = ref('')
const statusFilter   = ref<OrderStatus | 'all'>('all')
const selectedOrder  = ref<AdminOrder | null>(null)
const updatingStatus = ref<string | null>(null)

const STATUS_OPTIONS: OrderStatus[] = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
const STATUS_LABELS: Record<OrderStatus | 'all', string> = {
  all: 'Todas', pending: 'Pendientes', processing: 'En proceso',
  shipped: 'Enviadas', delivered: 'Entregadas', cancelled: 'Canceladas',
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('es-MX', { day: 'numeric', month: 'short', year: 'numeric' })
}

function formatAddress(addr: AdminOrder['shipping_address']): string {
  const parts = [addr.line1]
  if (addr.line2) parts.push(addr.line2)
  parts.push(`${addr.city}, ${addr.state} ${addr.zip}`)
  return parts.join(', ')
}

function orderTotal(o: AdminOrder): number {
  return Number(o.total_usd)
}

function totalItems(o: AdminOrder): number {
  return o.items.reduce((s, i) => s + i.qty, 0)
}

const filtered = computed(() => {
  let list = store.orders
  if (statusFilter.value !== 'all') list = list.filter(o => o.status === statusFilter.value)
  if (search.value) {
    const q = search.value.toLowerCase()
    list = list.filter(o =>
      o.id.toLowerCase().includes(q) ||
      (o.customer_name ?? '').toLowerCase().includes(q) ||
      o.customer_email.toLowerCase().includes(q)
    )
  }
  return list
})

const counts = computed(() => {
  const c: Record<string, number> = { all: store.orders.length }
  STATUS_OPTIONS.forEach(s => { c[s] = store.orders.filter(o => o.status === s).length })
  return c
})

async function updateStatus(order: AdminOrder, status: OrderStatus) {
  updatingStatus.value = order.id
  await store.changeStatus(order.id, status)
  if (selectedOrder.value?.id === order.id) {
    selectedOrder.value = store.orders.find(o => o.id === order.id) ?? null
  }
  updatingStatus.value = null
}

onMounted(() => store.loadOrders())
</script>

<template>
  <div class="space-y-5">

    <!-- KPI cards -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
      <AdminStatCard
        label="Pendientes"
        :value="String(counts.pending ?? 0)"
        sub="aguardando proceso"
        icon="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
        :value-color="(counts.pending ?? 0) > 0 ? 'var(--status-warn-text)' : undefined"
      />
      <AdminStatCard
        label="En Proceso"
        :value="String(counts.processing ?? 0)"
        sub="en preparación"
        icon="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
      />
      <AdminStatCard
        label="Enviadas"
        :value="String(counts.shipped ?? 0)"
        sub="en camino"
        icon="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0"
      />
      <AdminStatCard
        label="Entregadas"
        :value="String(counts.delivered ?? 0)"
        sub="completadas"
        icon="M5 13l4 4L19 7"
      />
    </div>

    <!-- Table card -->
    <div class="bg-white rounded-xl overflow-hidden" style="box-shadow: var(--admin-card-shadow);">
      <div class="px-6 py-4 flex items-center justify-between flex-wrap gap-3" style="border-bottom: 1px solid var(--admin-border);">
        <p class="text-[0.72rem] font-semibold uppercase tracking-wider" style="color: var(--admin-text-primary);">Historial de Órdenes</p>
        <span class="text-[0.72rem]" style="color: var(--admin-text-secondary);">{{ store.total }} total</span>
      </div>

      <!-- Filters -->
      <div class="px-6 py-3 flex items-center gap-3 flex-wrap" style="border-bottom: 1px solid var(--admin-border);">
        <AdminFilterBar v-model="search" placeholder="Buscar orden o cliente…">
          <select
            v-model="statusFilter"
            class="h-8 px-3 text-[0.75rem] rounded-lg appearance-none cursor-pointer focus:outline-none"
            style="border: 1.5px solid rgba(0,0,0,0.1); color: var(--admin-text-primary); background: white;"
          >
            <option value="all">Todos los estados</option>
            <option v-for="s in STATUS_OPTIONS" :key="s" :value="s">{{ STATUS_LABELS[s] }}</option>
          </select>
        </AdminFilterBar>
      </div>

      <!-- Error -->
      <div v-if="store.error" class="px-6 py-4 text-[0.82rem] text-red-600">{{ store.error }}</div>

      <!-- Skeleton -->
      <div v-else-if="store.loading" class="space-y-1 p-4">
        <div v-for="i in 5" :key="i" class="h-14 rounded-lg animate-pulse" style="background: rgba(0,0,0,0.05);" />
      </div>

      <!-- Empty -->
      <div v-else-if="filtered.length === 0" class="py-12 text-center text-[0.85rem]" style="color: var(--admin-text-secondary);">
        Sin órdenes{{ statusFilter !== 'all' ? ` con estado "${STATUS_LABELS[statusFilter]}"` : '' }}.
      </div>

      <!-- Table -->
      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr style="background: var(--admin-bg);">
              <th class="px-5 py-3 text-left font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Orden</th>
              <th class="px-5 py-3 text-left font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Cliente</th>
              <th class="px-5 py-3 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Artículos</th>
              <th class="px-5 py-3 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Total</th>
              <th class="px-5 py-3 text-center font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Estado</th>
              <th class="px-5 py-3 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Fecha</th>
              <th class="px-5 py-3 text-center font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Detalle</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="order in filtered"
              :key="order.id"
              class="cursor-pointer transition-colors duration-100"
              style="border-bottom: 1px solid rgba(0,0,0,0.04);"
              @click="selectedOrder = order"
            >
              <td class="px-5 py-3.5 font-mono text-[0.68rem] font-medium" style="color: var(--admin-text-primary);">{{ order.id.slice(0, 8) }}…</td>
              <td class="px-5 py-3.5">
                <p class="text-[0.82rem] font-medium" style="color: var(--admin-text-primary);">{{ order.customer_name ?? order.customer_email }}</p>
                <p class="text-[0.7rem]" style="color: var(--admin-text-secondary);">{{ order.customer_email }}</p>
              </td>
              <td class="px-5 py-3.5 text-right text-[0.82rem]" style="color: var(--admin-text-secondary);">
                {{ totalItems(order) }} pzas
              </td>
              <td class="px-5 py-3.5 text-right text-[0.82rem] font-medium" style="color: var(--admin-text-primary);">
                ${{ orderTotal(order).toFixed(2) }}
              </td>
              <td class="px-5 py-3.5 text-center">
                <StatusBadge :status="STATUS_MAP[order.status]" />
              </td>
              <td class="px-5 py-3.5 text-right text-[0.75rem]" style="color: var(--admin-text-secondary);">{{ formatDate(order.created_at) }}</td>
              <td class="px-5 py-3.5 text-center">
                <button
                  class="w-7 h-7 rounded-lg flex items-center justify-center mx-auto transition-colors"
                  style="background: rgba(0,0,0,0.05); color: var(--admin-text-secondary);"
                  @click.stop="selectedOrder = order"
                >
                  <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Order Detail Modal -->
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="selectedOrder" class="fixed inset-0 z-50 flex items-center justify-end">
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="selectedOrder = null" />
        <div class="relative w-full max-w-md h-full bg-white shadow-2xl overflow-y-auto flex flex-col">
          <!-- Header -->
          <div class="flex items-center justify-between px-6 py-4 flex-shrink-0" style="border-bottom: 1px solid var(--admin-border);">
            <div>
              <p class="font-mono text-[0.68rem] font-medium" style="color: var(--admin-text-secondary);">{{ selectedOrder.id }}</p>
              <p class="text-[1rem] font-bold mt-0.5" style="color: var(--admin-text-primary);">{{ selectedOrder.customer_name ?? selectedOrder.customer_email }}</p>
            </div>
            <button class="text-xl" style="color: var(--admin-text-secondary);" @click="selectedOrder = null">✕</button>
          </div>

          <div class="flex-1 p-6 space-y-6">
            <!-- Status + date -->
            <div class="flex items-center justify-between">
              <StatusBadge :status="STATUS_MAP[selectedOrder.status]" />
              <p class="text-[0.75rem]" style="color: var(--admin-text-secondary);">{{ formatDate(selectedOrder.created_at) }}</p>
            </div>

            <!-- Items -->
            <div>
              <p class="text-[0.65rem] font-semibold uppercase tracking-wider mb-3" style="color: var(--admin-text-secondary);">Artículos ({{ totalItems(selectedOrder) }} pzas)</p>
              <div class="space-y-2">
                <div
                  v-for="(item, i) in selectedOrder.items"
                  :key="item.id"
                  class="flex items-center justify-between text-[0.78rem]"
                >
                  <div>
                    <p class="font-medium" style="color: var(--admin-text-primary);">Artículo #{{ i + 1 }}</p>
                    <p style="color: var(--admin-text-secondary);">ID: {{ item.variant_id.slice(0, 8) }}… · ×{{ item.qty }}</p>
                  </div>
                  <p class="font-medium" style="color: var(--admin-text-primary);">${{ (Number(item.unit_price_usd) * item.qty).toFixed(2) }}</p>
                </div>
              </div>
            </div>

            <!-- Totals -->
            <div class="rounded-xl p-4 space-y-2" style="background: var(--admin-bg);">
              <div class="flex justify-between text-[0.78rem]" style="color: var(--admin-text-secondary);">
                <span>Subtotal</span><span>${{ Number(selectedOrder.subtotal_usd).toFixed(2) }}</span>
              </div>
              <div v-if="Number(selectedOrder.shipping_usd) > 0" class="flex justify-between text-[0.78rem]" style="color: var(--admin-text-secondary);">
                <span>Envío</span><span>${{ Number(selectedOrder.shipping_usd).toFixed(2) }}</span>
              </div>
              <div v-else class="flex justify-between text-[0.78rem]" style="color: var(--status-ok-text);">
                <span>Envío</span><span>Gratis</span>
              </div>
              <div v-if="Number(selectedOrder.discount_usd) > 0" class="flex justify-between text-[0.78rem]" style="color: var(--status-ok-text);">
                <span>Descuento</span><span>-${{ Number(selectedOrder.discount_usd).toFixed(2) }}</span>
              </div>
              <div class="flex justify-between text-[0.88rem] font-bold pt-1" style="border-top: 1px solid var(--admin-border); color: var(--admin-text-primary); padding-top: 8px; margin-top: 8px;">
                <span>Total</span>
                <span>${{ Number(selectedOrder.total_usd).toFixed(2) }}</span>
              </div>
            </div>

            <!-- Tracking -->
            <div v-if="selectedOrder.carrier_tracking_number">
              <p class="text-[0.65rem] font-semibold uppercase tracking-wider mb-1" style="color: var(--admin-text-secondary);">Tracking</p>
              <p class="font-mono text-[0.78rem]" style="color: var(--admin-text-primary);">{{ selectedOrder.carrier_tracking_number }}</p>
              <a v-if="selectedOrder.envia_label_url" :href="selectedOrder.envia_label_url" target="_blank" class="text-[0.72rem] font-medium" style="color: var(--admin-amber);">Ver etiqueta →</a>
            </div>

            <!-- Address -->
            <div>
              <p class="text-[0.65rem] font-semibold uppercase tracking-wider mb-2" style="color: var(--admin-text-secondary);">Dirección</p>
              <p class="text-[0.78rem] font-medium" style="color: var(--admin-text-primary);">{{ selectedOrder.shipping_address.full_name }}</p>
              <p class="text-[0.78rem]" style="color: var(--admin-text-secondary);">{{ formatAddress(selectedOrder.shipping_address) }}</p>
            </div>

            <!-- Update status -->
            <div>
              <p class="text-[0.65rem] font-semibold uppercase tracking-wider mb-2" style="color: var(--admin-text-secondary);">Actualizar estado</p>
              <div class="flex flex-wrap gap-2">
                <button
                  v-for="s in STATUS_OPTIONS"
                  :key="s"
                  class="px-3 py-1.5 text-[0.7rem] rounded-lg font-medium uppercase tracking-wider transition-all duration-150 disabled:opacity-50"
                  :style="selectedOrder.status === s
                    ? { background: 'var(--admin-amber)', color: '#fff', border: 'none' }
                    : { border: '1.5px solid rgba(0,0,0,0.12)', color: 'var(--admin-text-secondary)', background: 'transparent' }"
                  :disabled="updatingStatus === selectedOrder.id"
                  @click="updateStatus(selectedOrder!, s)"
                >{{ STATUS_LABELS[s] }}</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-enter-active { transition: opacity 0.2s ease, transform 0.2s ease; }
.modal-leave-active { transition: opacity 0.15s ease, transform 0.15s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
</style>
