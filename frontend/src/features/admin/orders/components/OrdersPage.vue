<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

type OrderStatus = 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled'

interface OrderItem {
  name: string
  size: string
  color: string
  qty: number
  priceUSD: number
}

interface Order {
  id: string
  customer: string
  email: string
  items: OrderItem[]
  subtotal: number
  shipping: number
  discount: number
  status: OrderStatus
  date: string
  address: string
}

const orders = ref<Order[]>([])
const loading = ref(true)
const statusFilter = ref<OrderStatus | 'all'>('all')
const selectedOrder = ref<Order | null>(null)
const updatingStatus = ref<string | null>(null)

const STATUS_COLORS: Record<OrderStatus, string> = {
  pending:    'text-amber-600 bg-amber-50 border-amber-200',
  processing: 'text-blue-600 bg-blue-50 border-blue-200',
  shipped:    'text-purple-600 bg-purple-50 border-purple-200',
  delivered:  'text-emerald-600 bg-emerald-50 border-emerald-200',
  cancelled:  'text-red-600 bg-red-50 border-red-200',
}

const STATUS_OPTIONS: OrderStatus[] = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']

const filtered = computed(() =>
  statusFilter.value === 'all'
    ? orders.value
    : orders.value.filter(o => o.status === statusFilter.value)
)

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
        id: 'V-2024-0318', customer: 'Carlos Mendoza',  email: 'carlos@example.com',
        items: [
          { name: 'Polo Atelier — Classic', size: 'M', color: 'Ivory', qty: 2, priceUSD: 180 },
          { name: 'Essential Tee',           size: 'M', color: 'Ivory', qty: 1, priceUSD: 95  },
        ],
        subtotal: 455, shipping: 0, discount: 0, status: 'delivered',
        date: 'Apr 11, 2024', address: '123 Reforma Ave, CDMX 06600',
      },
      {
        id: 'V-2024-0317', customer: 'Andrés Fuentes',  email: 'andres@example.com',
        items: [{ name: 'Signature Shirt', size: 'L', color: 'Midnight', qty: 1, priceUSD: 220 }],
        subtotal: 220, shipping: 12.99, discount: 0, status: 'shipped',
        date: 'Apr 11, 2024', address: '456 Insurgentes Sur, CDMX 03100',
      },
      {
        id: 'V-2024-0316', customer: 'Miguel Torres',   email: 'miguel@example.com',
        items: [
          { name: 'Polo Atelier — Design', size: 'M', color: 'Obsidian', qty: 2, priceUSD: 195 },
          { name: 'Essential Tee',          size: 'S', color: 'Warm Beige', qty: 3, priceUSD: 95 },
        ],
        subtotal: 675, shipping: 0, discount: 45, status: 'processing',
        date: 'Apr 10, 2024', address: '789 Polanco, CDMX 11560',
      },
      {
        id: 'V-2024-0315', customer: 'Ricardo Salinas', email: 'ricardo@example.com',
        items: [
          { name: 'Signature Shirt', size: 'M', color: 'Midnight', qty: 1, priceUSD: 220 },
          { name: 'Polo Atelier — Classic', size: 'L', color: 'Obsidian', qty: 1, priceUSD: 180 },
        ],
        subtotal: 400, shipping: 12.99, discount: 0, status: 'pending',
        date: 'Apr 10, 2024', address: '321 Santa Fe, CDMX 01210',
      },
      {
        id: 'V-2024-0313', customer: 'Luis Herrera',    email: 'luis@example.com',
        items: [{ name: 'Signature Shirt', size: 'L', color: 'Midnight', qty: 1, priceUSD: 220 }],
        subtotal: 220, shipping: 12.99, discount: 22, status: 'cancelled',
        date: 'Apr 9, 2024', address: '654 Lomas, CDMX 11000',
      },
    ]
    loading.value = false
  }, 400)
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div>
      <p class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)]">Fulfillment</p>
      <h1 class="mt-1 text-2xl font-semibold uppercase tracking-wider text-[color:var(--color-obsidian)]">Orders</h1>
    </div>

    <!-- Status tabs -->
    <div class="flex flex-wrap gap-2">
      <button
        v-for="tab in ['all', ...STATUS_OPTIONS]"
        :key="tab"
        class="flex items-center gap-1.5 px-3 py-1.5 text-xs uppercase tracking-widest rounded-[var(--radius-md)] border transition-colors duration-[var(--duration-fast)]"
        :class="statusFilter === tab
          ? 'bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] border-[color:var(--color-obsidian)]'
          : 'border-[color:var(--color-border)] text-[color:var(--color-border-strong)] hover:border-[color:var(--color-obsidian)] hover:text-[color:var(--color-obsidian)]'"
        @click="statusFilter = tab as any"
      >
        {{ tab }}
        <span class="font-semibold">{{ counts[tab] ?? 0 }}</span>
      </button>
    </div>

    <!-- Skeleton -->
    <div v-if="loading" class="space-y-3">
      <div v-for="i in 5" :key="i" class="h-16 rounded-[var(--radius-md)] bg-[color:var(--color-warm-beige-dk)] animate-pulse" />
    </div>

    <!-- Table -->
    <div v-else class="bg-[color:var(--color-ivory)] border border-[color:var(--color-border)] rounded-[var(--radius-md)] overflow-hidden">
      <div v-if="filtered.length === 0" class="py-12 text-center text-sm text-[color:var(--color-border-strong)]">
        No {{ statusFilter !== 'all' ? statusFilter : '' }} orders.
      </div>
      <table v-else class="w-full text-sm">
        <thead>
          <tr class="bg-[color:var(--color-warm-beige)] text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] border-b border-[color:var(--color-border)]">
            <th class="px-5 py-3 text-left font-medium">Order</th>
            <th class="px-5 py-3 text-left font-medium">Customer</th>
            <th class="px-5 py-3 text-right font-medium">Items</th>
            <th class="px-5 py-3 text-right font-medium">Total</th>
            <th class="px-5 py-3 text-center font-medium">Status</th>
            <th class="px-5 py-3 text-right font-medium">Date</th>
            <th class="px-5 py-3 text-right font-medium">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-[color:var(--color-border)]">
          <tr
            v-for="order in filtered"
            :key="order.id"
            class="hover:bg-[color:var(--color-warm-beige)] transition-colors duration-[var(--duration-fast)] cursor-pointer"
            @click="selectedOrder = order"
          >
            <td class="px-5 py-3.5 font-mono text-xs text-[color:var(--color-obsidian)]">{{ order.id }}</td>
            <td class="px-5 py-3.5">
              <p class="text-[color:var(--color-obsidian)] font-medium">{{ order.customer }}</p>
              <p class="text-xs text-[color:var(--color-border-strong)]">{{ order.email }}</p>
            </td>
            <td class="px-5 py-3.5 text-right text-[color:var(--color-border-strong)]">{{ order.items.reduce((s, i) => s + i.qty, 0) }}</td>
            <td class="px-5 py-3.5 text-right font-medium text-[color:var(--color-obsidian)]">${{ (order.subtotal + order.shipping - order.discount).toFixed(2) }}</td>
            <td class="px-5 py-3.5">
              <div class="flex justify-center">
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium uppercase tracking-wider border"
                  :class="STATUS_COLORS[order.status]"
                >{{ order.status }}</span>
              </div>
            </td>
            <td class="px-5 py-3.5 text-right text-xs text-[color:var(--color-border-strong)]">{{ order.date }}</td>
            <td class="px-5 py-3.5 text-right" @click.stop>
              <select
                :value="order.status"
                :disabled="updatingStatus === order.id"
                class="text-xs border border-[color:var(--color-border)] rounded-[var(--radius-sm)] px-2 py-1 bg-[color:var(--color-ivory)] focus:outline-none focus:border-[color:var(--color-obsidian)] disabled:opacity-50 cursor-pointer"
                @change="updateStatus(order, ($event.target as HTMLSelectElement).value as OrderStatus)"
              >
                <option v-for="s in STATUS_OPTIONS" :key="s" :value="s">{{ s }}</option>
              </select>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Order detail modal -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div v-if="selectedOrder" class="fixed inset-0 z-50 flex items-start justify-end">
          <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="selectedOrder = null" />
          <div class="relative w-full max-w-lg h-full bg-[color:var(--color-ivory)] shadow-2xl overflow-y-auto flex flex-col">
            <!-- Modal header -->
            <div class="sticky top-0 bg-[color:var(--color-ivory)] border-b border-[color:var(--color-border)] px-6 py-4 flex items-center justify-between z-10">
              <div>
                <p class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)]">Order Detail</p>
                <p class="font-mono text-sm font-medium text-[color:var(--color-obsidian)] mt-0.5">{{ selectedOrder.id }}</p>
              </div>
              <button class="p-1.5 hover:opacity-70 transition-opacity" @click="selectedOrder = null">
                <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>

            <div class="flex-1 px-6 py-6 space-y-6">
              <!-- Customer -->
              <div class="space-y-1">
                <p class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)]">Customer</p>
                <p class="font-medium text-[color:var(--color-obsidian)]">{{ selectedOrder.customer }}</p>
                <p class="text-sm text-[color:var(--color-border-strong)]">{{ selectedOrder.email }}</p>
                <p class="text-sm text-[color:var(--color-border-strong)]">{{ selectedOrder.address }}</p>
              </div>

              <!-- Status -->
              <div class="space-y-2">
                <p class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)]">Status</p>
                <div class="flex items-center gap-3">
                  <span
                    class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium uppercase tracking-wider border"
                    :class="STATUS_COLORS[selectedOrder.status]"
                  >{{ selectedOrder.status }}</span>
                  <select
                    :value="selectedOrder.status"
                    class="text-xs border border-[color:var(--color-border)] rounded-[var(--radius-sm)] px-2 py-1 bg-[color:var(--color-ivory)] focus:outline-none focus:border-[color:var(--color-obsidian)] cursor-pointer"
                    @change="updateStatus(selectedOrder, ($event.target as HTMLSelectElement).value as OrderStatus)"
                  >
                    <option v-for="s in STATUS_OPTIONS" :key="s" :value="s">{{ s }}</option>
                  </select>
                </div>
              </div>

              <!-- Items -->
              <div>
                <p class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] mb-3">Items</p>
                <div class="space-y-2">
                  <div
                    v-for="item in selectedOrder.items"
                    :key="`${item.name}-${item.size}-${item.color}`"
                    class="flex items-center justify-between py-2 border-b border-[color:var(--color-border)]"
                  >
                    <div>
                      <p class="text-sm font-medium text-[color:var(--color-obsidian)]">{{ item.name }}</p>
                      <p class="text-xs text-[color:var(--color-border-strong)]">{{ item.size }} · {{ item.color }} · ×{{ item.qty }}</p>
                    </div>
                    <p class="text-sm font-medium">${{ (item.priceUSD * item.qty).toFixed(2) }}</p>
                  </div>
                </div>
              </div>

              <!-- Totals -->
              <div class="space-y-1.5 pt-2">
                <div class="flex justify-between text-sm text-[color:var(--color-border-strong)]">
                  <span>Subtotal</span><span>${{ selectedOrder.subtotal.toFixed(2) }}</span>
                </div>
                <div class="flex justify-between text-sm text-[color:var(--color-border-strong)]">
                  <span>Shipping</span>
                  <span>{{ selectedOrder.shipping === 0 ? 'Free' : `$${selectedOrder.shipping.toFixed(2)}` }}</span>
                </div>
                <div v-if="selectedOrder.discount > 0" class="flex justify-between text-sm text-emerald-600">
                  <span>Discount</span><span>-${{ selectedOrder.discount.toFixed(2) }}</span>
                </div>
                <div class="flex justify-between text-base font-semibold text-[color:var(--color-obsidian)] pt-2 border-t border-[color:var(--color-border)]">
                  <span>Total</span>
                  <span>${{ (selectedOrder.subtotal + selectedOrder.shipping - selectedOrder.discount).toFixed(2) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.modal-fade-enter-active { transition: opacity var(--duration-normal) ease; }
.modal-fade-leave-active { transition: opacity var(--duration-fast) ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }
</style>
