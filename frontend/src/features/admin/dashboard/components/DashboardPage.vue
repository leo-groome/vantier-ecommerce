<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import AdminStatCard from '@features/admin/components/shared/AdminStatCard.vue'
import StatusBadge from '@features/admin/components/shared/StatusBadge.vue'
import AdminButton from '@features/admin/components/shared/AdminButton.vue'
import type { AdminStatus } from '@features/admin/components/shared/StatusBadge.vue'

interface KPI {
  label: string; value: string; sub: string
  delta?: string; deltaUp?: boolean; icon: string
  valueColor?: string
}

interface RecentOrder {
  id: string; customer: string; items: number
  total: number; status: AdminStatus; date: string
}

const kpis = ref<KPI[]>([])
const recentOrders = ref<RecentOrder[]>([])
const loading = ref(true)

onMounted(() => {
  setTimeout(() => {
    kpis.value = [
      {
        label: 'Revenue Hoy',
        value: '$3,240', sub: '18 órdenes', delta: '+12%', deltaUp: true,
        icon: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
      },
      {
        label: 'Órdenes este mes',
        value: '342', sub: '$58,400 total', delta: '+8%', deltaUp: true,
        icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',
      },
      {
        label: 'Stock Bajo',
        value: '7', sub: 'variantes ≤ 5 uds', delta: '+3', deltaUp: false,
        valueColor: 'var(--status-warn-text)',
        icon: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z',
      },
      {
        label: 'Exchanges Pendientes',
        value: '4', sub: 'pendientes aprobación', delta: '-2', deltaUp: true,
        icon: 'M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4',
      },
    ]

    recentOrders.value = [
      { id: 'V-2024-0318', customer: 'Carlos Mendoza',  items: 3, total: 555,  status: 'entregado',  date: 'Abr 11' },
      { id: 'V-2024-0317', customer: 'Andrés Fuentes',  items: 1, total: 180,  status: 'enviado',    date: 'Abr 11' },
      { id: 'V-2024-0316', customer: 'Miguel Torres',   items: 5, total: 875,  status: 'procesando', date: 'Abr 10' },
      { id: 'V-2024-0315', customer: 'Ricardo Salinas', items: 2, total: 415,  status: 'pendiente',  date: 'Abr 10' },
      { id: 'V-2024-0314', customer: 'Javier Ríos',     items: 4, total: 760,  status: 'procesando', date: 'Abr 10' },
      { id: 'V-2024-0313', customer: 'Luis Herrera',    items: 1, total: 220,  status: 'enviado',    date: 'Abr 9'  },
      { id: 'V-2024-0312', customer: 'Fernando López',  items: 6, total: 1090, status: 'entregado',  date: 'Abr 9'  },
    ]
    loading.value = false
  }, 400)
})
</script>

<template>
  <div class="space-y-6">

    <!-- Page header -->
    <div class="flex items-end justify-between">
      <div>
        <h1 class="text-[1.5rem] font-bold" style="color: var(--admin-text-primary);">Dashboard</h1>
        <p class="text-[0.8rem] mt-0.5" style="color: var(--admin-text-secondary);">Vista general del negocio</p>
      </div>
    </div>

    <!-- KPI skeleton -->
    <div v-if="loading" class="grid grid-cols-2 xl:grid-cols-4 gap-4">
      <div v-for="i in 4" :key="i" class="h-28 rounded-xl animate-pulse" style="background: rgba(0,0,0,0.06);" />
    </div>

    <!-- KPI cards -->
    <div v-else class="grid grid-cols-2 xl:grid-cols-4 gap-4">
      <AdminStatCard
        v-for="kpi in kpis"
        :key="kpi.label"
        :label="kpi.label"
        :value="kpi.value"
        :sub="kpi.sub"
        :delta="kpi.delta"
        :delta-up="kpi.deltaUp"
        :icon="kpi.icon"
        :value-color="kpi.valueColor"
      />
    </div>

    <!-- Recent orders -->
    <div class="bg-white rounded-xl overflow-hidden" style="box-shadow: var(--admin-card-shadow);">
      <div class="px-6 py-4 flex items-center justify-between" style="border-bottom: 1px solid var(--admin-border);">
        <p class="text-[0.75rem] font-semibold uppercase tracking-wider" style="color: var(--admin-text-primary);">Órdenes Recientes</p>
        <RouterLink
          to="/admin/orders"
          class="text-[0.72rem] font-medium transition-colors"
          style="color: var(--admin-amber);"
        >Ver todas →</RouterLink>
      </div>

      <!-- Skeleton -->
      <div v-if="loading" class="divide-y" style="border-color: var(--admin-border);">
        <div v-for="i in 5" :key="i" class="px-6 py-4 flex gap-4">
          <div class="h-3 w-28 rounded animate-pulse" style="background: rgba(0,0,0,0.06);" />
          <div class="h-3 w-40 rounded animate-pulse" style="background: rgba(0,0,0,0.06);" />
        </div>
      </div>

      <!-- Table -->
      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr style="background: var(--admin-bg);">
              <th class="px-6 py-3 text-left font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Orden</th>
              <th class="px-6 py-3 text-left font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Cliente</th>
              <th class="px-6 py-3 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Items</th>
              <th class="px-6 py-3 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Total</th>
              <th class="px-6 py-3 text-center font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Estado</th>
              <th class="px-6 py-3 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Fecha</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="order in recentOrders"
              :key="order.id"
              class="transition-colors duration-100"
              style="border-bottom: 1px solid rgba(0,0,0,0.04);"
            >
              <td class="px-6 py-3.5 font-mono text-[0.72rem] font-medium" style="color: var(--admin-text-primary);">{{ order.id }}</td>
              <td class="px-6 py-3.5 text-[0.82rem]" style="color: var(--admin-text-primary);">{{ order.customer }}</td>
              <td class="px-6 py-3.5 text-right text-[0.82rem]" style="color: var(--admin-text-secondary);">{{ order.items }}</td>
              <td class="px-6 py-3.5 text-right text-[0.82rem] font-medium" style="color: var(--admin-text-primary);">${{ order.total.toLocaleString() }}</td>
              <td class="px-6 py-3.5">
                <div class="flex justify-center">
                  <StatusBadge :status="order.status" />
                </div>
              </td>
              <td class="px-6 py-3.5 text-right text-[0.75rem]" style="color: var(--admin-text-secondary);">{{ order.date }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Quick actions -->
    <div class="flex items-center gap-3 flex-wrap">
      <RouterLink to="/admin/inventory">
        <AdminButton variant="primary">
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          Agregar Producto
        </AdminButton>
      </RouterLink>
      <RouterLink to="/admin/orders">
        <AdminButton variant="ghost">Ver Órdenes</AdminButton>
      </RouterLink>
      <RouterLink to="/admin/discounts">
        <AdminButton variant="ghost">Crear Descuento</AdminButton>
      </RouterLink>
    </div>

  </div>
</template>
