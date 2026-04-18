<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminStatCard from '@features/admin/components/shared/AdminStatCard.vue'
import StatusBadge from '@features/admin/components/shared/StatusBadge.vue'
import AdminButton from '@features/admin/components/shared/AdminButton.vue'
import AdminFilterBar from '@features/admin/components/shared/AdminFilterBar.vue'
import type { AdminStatus } from '@features/admin/components/shared/StatusBadge.vue'

type OrderStatus = 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled'

const STATUS_MAP: Record<OrderStatus, AdminStatus> = {
  pending:    'pendiente',
  processing: 'procesando',
  shipped:    'enviado',
  delivered:  'entregado',
  cancelled:  'inactivo',
}

interface OrderItem { name: string; size: string; color: string; qty: number; priceUSD: number }
interface Order {
  id: string; customer: string; email: string
  items: OrderItem[]; subtotal: number; shipping: number; discount: number
  status: OrderStatus; date: string; address: string
}

const orders         = ref<Order[]>([])
const loading        = ref(true)
const search         = ref('')
const statusFilter   = ref<OrderStatus | 'all'>('all')
const selectedOrder  = ref<Order | null>(null)
const updatingStatus = ref<string | null>(null)

const STATUS_OPTIONS: OrderStatus[] = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
const STATUS_LABELS: Record<OrderStatus | 'all', string> = {
  all: 'Todas', pending: 'Pendientes', processing: 'En proceso',
  shipped: 'Enviadas', delivered: 'Entregadas', cancelled: 'Canceladas',
}

const filtered = computed(() => {
  let list = orders.value
  if (statusFilter.value !== 'all') list = list.filter(o => o.status === statusFilter.value)
  if (search.value) {
    const q = search.value.toLowerCase()
    list = list.filter(o => o.id.toLowerCase().includes(q) || o.customer.toLowerCase().includes(q))
  }
  return list
})

const counts = computed(() => {
  const c: Record<string, number> = { all: orders.value.length }
  STATUS_OPTIONS.forEach(s => { c[s] = orders.value.filter(o => o.status === s).length })
  return c
})

async function updateStatus(order: Order, status: OrderStatus) {
  updatingStatus.value = order.id
  await new Promise(r => setTimeout(r, 400))
  order.status = status
  updatingStatus.value = null
}

onMounted(() => {
  setTimeout(() => {
    orders.value = [
      {
        id: 'V-2024-0318', customer: 'Carlos Mendoza', email: 'carlos@example.com',
        items: [
          { name: 'Polo Atelier — Classic', size: 'M', color: 'Ivory',   qty: 2, priceUSD: 180 },
          { name: 'Essential Tee',          size: 'M', color: 'Ivory',   qty: 1, priceUSD: 95  },
        ],
        subtotal: 455, shipping: 0, discount: 0, status: 'delivered',
        date: 'Abr 11, 2026', address: '123 Reforma Ave, CDMX 06600',
      },
      {
        id: 'V-2024-0317', customer: 'Andrés Fuentes', email: 'andres@example.com',
        items: [{ name: 'Signature Shirt', size: 'L', color: 'Midnight', qty: 1, priceUSD: 220 }],
        subtotal: 220, shipping: 12.99, discount: 0, status: 'shipped',
        date: 'Abr 11, 2026', address: '456 Insurgentes Sur, CDMX 03100',
      },
      {
        id: 'V-2024-0316', customer: 'Miguel Torres', email: 'miguel@example.com',
        items: [
          { name: 'Polo Atelier — Design', size: 'M', color: 'Obsidian',   qty: 2, priceUSD: 195 },
          { name: 'Essential Tee',         size: 'S', color: 'Warm Beige', qty: 3, priceUSD: 95  },
        ],
        subtotal: 675, shipping: 0, discount: 45, status: 'processing',
        date: 'Abr 10, 2026', address: '789 Polanco, CDMX 11560',
      },
      {
        id: 'V-2024-0315', customer: 'Ricardo Salinas', email: 'ricardo@example.com',
        items: [
          { name: 'Signature Shirt',       size: 'M', color: 'Midnight', qty: 1, priceUSD: 220 },
          { name: 'Polo Atelier — Classic', size: 'L', color: 'Obsidian', qty: 1, priceUSD: 180 },
        ],
        subtotal: 400, shipping: 12.99, discount: 0, status: 'pending',
        date: 'Abr 10, 2026', address: '321 Santa Fe, CDMX 01210',
      },
      {
        id: 'V-2024-0313', customer: 'Luis Herrera', email: 'luis@example.com',
        items: [{ name: 'Signature Shirt', size: 'L', color: 'Midnight', qty: 1, priceUSD: 220 }],
        subtotal: 220, shipping: 12.99, discount: 22, status: 'cancelled',
        date: 'Abr 9, 2026', address: '654 Lomas, CDMX 11000',
      },
      {
        id: 'V-2024-0312', customer: 'Fernando López', email: 'fernando@example.com',
        items: [
          { name: 'Polo Atelier — Classic', size: 'XL', color: 'Obsidian', qty: 3, priceUSD: 180 },
          { name: 'Essential Tee',          size: 'XL', color: 'Ivory',    qty: 3, priceUSD: 95  },
        ],
        subtotal: 825, shipping: 0, discount: 0, status: 'delivered',
        date: 'Abr 9, 2026', address: '987 Condesa, CDMX 06140',
      },
      {
        id: 'V-2024-0311', customer: 'Javier Ríos', email: 'javier@example.com',
        items: [{ name: 'Polo Atelier — Design', size: 'L', color: 'Midnight', qty: 2, priceUSD: 195 }],
        subtotal: 390, shipping: 12.99, discount: 0, status: 'processing',
        date: 'Abr 8, 2026', address: '159 Del Valle, CDMX 03100',
      },
      {
        id: 'V-2024-0310', customer: 'Marcos Vega', email: 'marcos@example.com',
        items: [{ name: 'Signature Shirt', size: 'M', color: 'Ivory', qty: 1, priceUSD: 220 }],
        subtotal: 220, shipping: 0, discount: 44, status: 'shipped',
        date: 'Abr 8, 2026', address: '357 Narvarte, CDMX 03600',
      },
      {
        id: 'V-2024-0309', customer: 'Sofía García', email: 'sofia@example.com',
        items: [{ name: 'Essential Tee', size: 'S', color: 'Ivory', qty: 2, priceUSD: 95 }],
        subtotal: 190, shipping: 12.99, discount: 0, status: 'pending',
        date: 'Abr 7, 2026', address: '246 Coyoacán, CDMX 04100',
      },
      {
        id: 'V-2024-0308', customer: 'Diego Morales', email: 'diego@example.com',
        items: [
          { name: 'Polo Atelier — Classic', size: 'L', color: 'Ivory',    qty: 1, priceUSD: 180 },
          { name: 'Polo Atelier — Classic', size: 'L', color: 'Obsidian', qty: 1, priceUSD: 180 },
          { name: 'Essential Tee',          size: 'L', color: 'Ivory',    qty: 2, priceUSD: 95  },
        ],
        subtotal: 550, shipping: 0, discount: 0, status: 'delivered',
        date: 'Abr 7, 2026', address: '468 Xochimilco, CDMX 16000',
      },
      {
        id: 'V-2024-0307', customer: 'Ana Ruiz', email: 'ana@example.com',
        items: [{ name: 'Signature Shirt', size: 'S', color: 'Midnight', qty: 1, priceUSD: 220 }],
        subtotal: 220, shipping: 12.99, discount: 0, status: 'processing',
        date: 'Abr 6, 2026', address: '135 Tlalpan, CDMX 14000',
      },
      {
        id: 'V-2024-0306', customer: 'Roberto Castro', email: 'roberto@example.com',
        items: [{ name: 'Polo Atelier — Design', size: 'M', color: 'Ivory', qty: 1, priceUSD: 195 }],
        subtotal: 195, shipping: 12.99, discount: 0, status: 'pending',
        date: 'Abr 6, 2026', address: '579 Tepito, CDMX 06820',
      },
    ]
    loading.value = false
  }, 400)
})
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
        sub="este mes"
        icon="M5 13l4 4L19 7"
      />
    </div>

    <!-- Table card -->
    <div class="bg-white rounded-xl overflow-hidden" style="box-shadow: var(--admin-card-shadow);">
      <div class="px-6 py-4 flex items-center justify-between flex-wrap gap-3" style="border-bottom: 1px solid var(--admin-border);">
        <p class="text-[0.72rem] font-semibold uppercase tracking-wider" style="color: var(--admin-text-primary);">Historial de Órdenes</p>
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

      <!-- Skeleton -->
      <div v-if="loading" class="space-y-1 p-4">
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
              <th class="px-5 py-3 text-center font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Acciones</th>
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
              <td class="px-5 py-3.5 font-mono text-[0.72rem] font-medium" style="color: var(--admin-text-primary);">{{ order.id }}</td>
              <td class="px-5 py-3.5">
                <p class="text-[0.82rem] font-medium" style="color: var(--admin-text-primary);">{{ order.customer }}</p>
                <p class="text-[0.7rem]" style="color: var(--admin-text-secondary);">{{ order.email }}</p>
              </td>
              <td class="px-5 py-3.5 text-right text-[0.82rem]" style="color: var(--admin-text-secondary);">
                {{ order.items.reduce((s, i) => s + i.qty, 0) }} pzas
              </td>
              <td class="px-5 py-3.5 text-right text-[0.82rem] font-medium" style="color: var(--admin-text-primary);">
                ${{ (order.subtotal + order.shipping - order.discount).toLocaleString() }}
              </td>
              <td class="px-5 py-3.5 text-center">
                <StatusBadge :status="STATUS_MAP[order.status]" />
              </td>
              <td class="px-5 py-3.5 text-right text-[0.75rem]" style="color: var(--admin-text-secondary);">{{ order.date }}</td>
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
              <p class="font-mono text-[0.72rem] font-medium" style="color: var(--admin-text-secondary);">{{ selectedOrder.id }}</p>
              <p class="text-[1rem] font-bold mt-0.5" style="color: var(--admin-text-primary);">{{ selectedOrder.customer }}</p>
            </div>
            <button class="text-xl" style="color: var(--admin-text-secondary);" @click="selectedOrder = null">✕</button>
          </div>

          <div class="flex-1 p-6 space-y-6">
            <!-- Status + date -->
            <div class="flex items-center justify-between">
              <StatusBadge :status="STATUS_MAP[selectedOrder.status]" />
              <p class="text-[0.75rem]" style="color: var(--admin-text-secondary);">{{ selectedOrder.date }}</p>
            </div>

            <!-- Items -->
            <div>
              <p class="text-[0.65rem] font-semibold uppercase tracking-wider mb-3" style="color: var(--admin-text-secondary);">Artículos</p>
              <div class="space-y-2">
                <div
                  v-for="(item, i) in selectedOrder.items"
                  :key="i"
                  class="flex items-center justify-between text-[0.78rem]"
                >
                  <div>
                    <p class="font-medium" style="color: var(--admin-text-primary);">{{ item.name }}</p>
                    <p style="color: var(--admin-text-secondary);">{{ item.size }} · {{ item.color }} · ×{{ item.qty }}</p>
                  </div>
                  <p class="font-medium" style="color: var(--admin-text-primary);">${{ (item.priceUSD * item.qty).toLocaleString() }}</p>
                </div>
              </div>
            </div>

            <!-- Totals -->
            <div class="rounded-xl p-4 space-y-2" style="background: var(--admin-bg);">
              <div class="flex justify-between text-[0.78rem]" style="color: var(--admin-text-secondary);">
                <span>Subtotal</span><span>${{ selectedOrder.subtotal.toLocaleString() }}</span>
              </div>
              <div v-if="selectedOrder.shipping" class="flex justify-between text-[0.78rem]" style="color: var(--admin-text-secondary);">
                <span>Envío</span><span>${{ selectedOrder.shipping.toFixed(2) }}</span>
              </div>
              <div v-if="selectedOrder.discount" class="flex justify-between text-[0.78rem]" style="color: var(--status-ok-text);">
                <span>Descuento</span><span>-${{ selectedOrder.discount.toLocaleString() }}</span>
              </div>
              <div class="flex justify-between text-[0.88rem] font-bold pt-1" style="border-top: 1px solid var(--admin-border); color: var(--admin-text-primary); padding-top: 8px; margin-top: 8px;">
                <span>Total</span>
                <span>${{ (selectedOrder.subtotal + selectedOrder.shipping - selectedOrder.discount).toLocaleString() }}</span>
              </div>
            </div>

            <!-- Address -->
            <div>
              <p class="text-[0.65rem] font-semibold uppercase tracking-wider mb-2" style="color: var(--admin-text-secondary);">Dirección</p>
              <p class="text-[0.78rem]" style="color: var(--admin-text-primary);">{{ selectedOrder.address }}</p>
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
