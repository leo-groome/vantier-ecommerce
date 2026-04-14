<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface KPI {
  label: string
  value: string
  sub: string
  delta?: string
  deltaUp?: boolean
  icon: string
}

interface RecentOrder {
  id: string
  customer: string
  items: number
  total: number
  status: 'pending' | 'processing' | 'shipped' | 'delivered'
  date: string
}

const kpis = ref<KPI[]>([])
const recentOrders = ref<RecentOrder[]>([])
const loading = ref(true)

const STATUS_COLORS: Record<string, string> = {
  pending:    'text-amber-600 bg-amber-50',
  processing: 'text-blue-600 bg-blue-50',
  shipped:    'text-purple-600 bg-purple-50',
  delivered:  'text-emerald-600 bg-emerald-50',
}

onMounted(() => {
  setTimeout(() => {
    kpis.value = [
      {
        label: 'Revenue Today',
        value: '$3,240',
        sub: '18 orders',
        delta: '+12%',
        deltaUp: true,
        icon: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
      },
      {
        label: 'Orders This Month',
        value: '342',
        sub: '$58,400 total',
        delta: '+8%',
        deltaUp: true,
        icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',
      },
      {
        label: 'Low Stock Items',
        value: '7',
        sub: 'Below 5 units',
        delta: '+3',
        deltaUp: false,
        icon: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4',
      },
      {
        label: 'Pending Exchanges',
        value: '4',
        sub: 'Awaiting approval',
        delta: '-2',
        deltaUp: true,
        icon: 'M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4',
      },
    ]

    recentOrders.value = [
      { id: 'V-2024-0318', customer: 'Carlos Mendoza',  items: 3, total: 555,  status: 'delivered',  date: 'Apr 11' },
      { id: 'V-2024-0317', customer: 'Andrés Fuentes',  items: 1, total: 180,  status: 'shipped',    date: 'Apr 11' },
      { id: 'V-2024-0316', customer: 'Miguel Torres',   items: 5, total: 875,  status: 'processing', date: 'Apr 10' },
      { id: 'V-2024-0315', customer: 'Ricardo Salinas', items: 2, total: 415,  status: 'pending',    date: 'Apr 10' },
      { id: 'V-2024-0314', customer: 'Javier Ríos',     items: 4, total: 760,  status: 'processing', date: 'Apr 10' },
      { id: 'V-2024-0313', customer: 'Luis Herrera',    items: 1, total: 220,  status: 'shipped',    date: 'Apr 9'  },
      { id: 'V-2024-0312', customer: 'Fernando López',  items: 6, total: 1090, status: 'delivered',  date: 'Apr 9'  },
    ]
    loading.value = false
  }, 400)
})
</script>

<template>
  <div class="space-y-8">
    <!-- Page header -->
    <div>
      <p class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)]">Overview</p>
      <h1 class="mt-1 text-2xl font-semibold uppercase tracking-wider text-[color:var(--color-obsidian)]">Dashboard</h1>
    </div>

    <!-- KPI cards skeleton -->
    <div v-if="loading" class="grid grid-cols-2 xl:grid-cols-4 gap-4">
      <div v-for="i in 4" :key="i" class="h-28 rounded-[var(--radius-md)] bg-[color:var(--color-warm-beige-dk)] animate-pulse" />
    </div>

    <!-- KPI cards -->
    <div v-else class="grid grid-cols-2 xl:grid-cols-4 gap-4">
      <div
        v-for="kpi in kpis"
        :key="kpi.label"
        class="bg-[color:var(--color-ivory)] border border-[color:var(--color-border)] rounded-[var(--radius-md)] p-5 flex flex-col gap-3"
      >
        <div class="flex items-start justify-between">
          <p class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)]">{{ kpi.label }}</p>
          <svg class="w-4 h-4 text-[color:var(--color-border-strong)] flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path :d="kpi.icon" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <div class="flex items-end justify-between gap-2">
          <div>
            <p class="text-3xl font-semibold tracking-tight text-[color:var(--color-obsidian)]">{{ kpi.value }}</p>
            <p class="mt-0.5 text-xs text-[color:var(--color-border-strong)]">{{ kpi.sub }}</p>
          </div>
          <span
            v-if="kpi.delta"
            class="text-xs font-medium px-2 py-0.5 rounded-full"
            :class="kpi.deltaUp ? 'bg-emerald-50 text-emerald-700' : 'bg-red-50 text-red-600'"
          >{{ kpi.delta }}</span>
        </div>
      </div>
    </div>

    <!-- Recent orders -->
    <div class="bg-[color:var(--color-ivory)] border border-[color:var(--color-border)] rounded-[var(--radius-md)] overflow-hidden">
      <div class="px-6 py-4 border-b border-[color:var(--color-border)] flex items-center justify-between">
        <p class="text-xs uppercase tracking-widest font-semibold text-[color:var(--color-obsidian)]">Recent Orders</p>
        <RouterLink to="/admin/orders" class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] hover:text-[color:var(--color-obsidian)] transition-colors">
          View all →
        </RouterLink>
      </div>

      <!-- Skeleton rows -->
      <div v-if="loading" class="divide-y divide-[color:var(--color-border)]">
        <div v-for="i in 5" :key="i" class="px-6 py-4 flex gap-4">
          <div class="h-3 w-28 bg-[color:var(--color-warm-beige-dk)] animate-pulse rounded" />
          <div class="h-3 w-40 bg-[color:var(--color-warm-beige-dk)] animate-pulse rounded" />
        </div>
      </div>

      <!-- Table -->
      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-[color:var(--color-warm-beige)] text-xs uppercase tracking-widest text-[color:var(--color-border-strong)]">
              <th class="px-6 py-3 text-left font-medium">Order</th>
              <th class="px-6 py-3 text-left font-medium">Customer</th>
              <th class="px-6 py-3 text-right font-medium">Items</th>
              <th class="px-6 py-3 text-right font-medium">Total</th>
              <th class="px-6 py-3 text-center font-medium">Status</th>
              <th class="px-6 py-3 text-right font-medium">Date</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-[color:var(--color-border)]">
            <tr
              v-for="order in recentOrders"
              :key="order.id"
              class="hover:bg-[color:var(--color-warm-beige)] transition-colors duration-[var(--duration-fast)]"
            >
              <td class="px-6 py-3.5 font-mono text-xs text-[color:var(--color-obsidian)]">{{ order.id }}</td>
              <td class="px-6 py-3.5 text-[color:var(--color-obsidian)]">{{ order.customer }}</td>
              <td class="px-6 py-3.5 text-right text-[color:var(--color-border-strong)]">{{ order.items }}</td>
              <td class="px-6 py-3.5 text-right font-medium text-[color:var(--color-obsidian)]">${{ order.total.toLocaleString() }}</td>
              <td class="px-6 py-3.5">
                <div class="flex justify-center">
                  <span
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium uppercase tracking-wider"
                    :class="STATUS_COLORS[order.status]"
                  >{{ order.status }}</span>
                </div>
              </td>
              <td class="px-6 py-3.5 text-right text-xs text-[color:var(--color-border-strong)]">{{ order.date }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Quick actions -->
    <div>
      <p class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] mb-3">Quick Actions</p>
      <div class="flex flex-wrap gap-3">
        <RouterLink
          to="/admin/inventory"
          class="flex items-center gap-2 px-4 py-2.5 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-xs uppercase tracking-widest rounded-[var(--radius-md)] hover:opacity-80 transition-opacity duration-[var(--duration-fast)]"
        >
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          Add Product
        </RouterLink>
        <RouterLink
          to="/admin/orders"
          class="flex items-center gap-2 px-4 py-2.5 border border-[color:var(--color-border)] text-xs uppercase tracking-widest rounded-[var(--radius-md)] hover:bg-[color:var(--color-warm-beige)] transition-colors duration-[var(--duration-fast)]"
        >
          View Orders
        </RouterLink>
        <RouterLink
          to="/admin/discounts"
          class="flex items-center gap-2 px-4 py-2.5 border border-[color:var(--color-border)] text-xs uppercase tracking-widest rounded-[var(--radius-md)] hover:bg-[color:var(--color-warm-beige)] transition-colors duration-[var(--duration-fast)]"
        >
          Create Discount
        </RouterLink>
      </div>
    </div>
  </div>
</template>
