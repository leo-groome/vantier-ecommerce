<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import AdminStatCard from '@features/admin/components/shared/AdminStatCard.vue'
import StatusBadge from '@features/admin/components/shared/StatusBadge.vue'
import AdminButton from '@features/admin/components/shared/AdminButton.vue'
import type { AdminStatus } from '@features/admin/components/shared/StatusBadge.vue'
import { useAdminDashboardStore } from '../store'

const store = useAdminDashboardStore()

const STATUS_MAP: Record<string, AdminStatus> = {
  pending:    'pendiente',
  processing: 'procesando',
  shipped:    'enviado',
  delivered:  'entregado',
  cancelled:  'inactivo',
}

const pendingCount = computed(() =>
  store.recentOrders.filter(o => o.status === 'pending').length
)

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('es-MX', { day: 'numeric', month: 'short' })
}

function orderTotal(o: { total_usd: string }): string {
  return `$${Number(o.total_usd).toFixed(2)}`
}

function totalItems(o: { items: { qty: number }[] }): number {
  return o.items.reduce((s, i) => s + i.qty, 0)
}

onMounted(() => store.loadDashboard())
</script>

<template>
  <div class="space-y-6">

    <!-- Quick actions -->
    <div class="flex items-center justify-end gap-3 flex-wrap">
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

    <!-- Error -->
    <div v-if="store.error" class="text-[0.82rem] text-red-600 px-1">{{ store.error }}</div>

    <!-- KPI skeleton -->
    <div v-if="store.loading" class="grid grid-cols-2 xl:grid-cols-4 gap-4">
      <div v-for="i in 4" :key="i" class="h-28 rounded-xl animate-pulse" style="background: rgba(0,0,0,0.06);" />
    </div>

    <!-- KPI cards -->
    <div v-else class="grid grid-cols-2 xl:grid-cols-4 gap-4">
      <AdminStatCard
        label="Total Órdenes"
        :value="String(store.totalOrders)"
        sub="en el sistema"
        icon="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
      />
      <AdminStatCard
        label="Pendientes"
        :value="String(pendingCount)"
        sub="aguardando proceso"
        :value-color="pendingCount > 0 ? 'var(--status-warn-text)' : undefined"
        icon="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
      />
      <AdminStatCard
        label="Stock Bajo"
        :value="String(store.lowStockCount)"
        sub="variantes ≤ 50 uds"
        :value-color="store.lowStockCount > 0 ? 'var(--status-warn-text)' : undefined"
        icon="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
      />
      <AdminStatCard
        label="Recientes"
        :value="String(store.recentOrders.length)"
        sub="últimas mostradas"
        icon="M13 10V3L4 14h7v7l9-11h-7z"
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
      <div v-if="store.loading" class="divide-y" style="border-color: var(--admin-border);">
        <div v-for="i in 5" :key="i" class="px-6 py-4 flex gap-4">
          <div class="h-3 w-28 rounded animate-pulse" style="background: rgba(0,0,0,0.06);" />
          <div class="h-3 w-40 rounded animate-pulse" style="background: rgba(0,0,0,0.06);" />
        </div>
      </div>

      <!-- Empty -->
      <div v-else-if="store.recentOrders.length === 0" class="py-10 text-center text-[0.85rem]" style="color: var(--admin-text-secondary);">
        Sin órdenes aún.
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
              v-for="order in store.recentOrders"
              :key="order.id"
              class="transition-colors duration-100"
              style="border-bottom: 1px solid rgba(0,0,0,0.04);"
            >
              <td class="px-6 py-3.5 font-mono text-[0.68rem] font-medium" style="color: var(--admin-text-primary);">{{ order.id.slice(0, 8) }}…</td>
              <td class="px-6 py-3.5 text-[0.82rem]" style="color: var(--admin-text-primary);">{{ order.customer_name ?? order.customer_email }}</td>
              <td class="px-6 py-3.5 text-right text-[0.82rem]" style="color: var(--admin-text-secondary);">{{ totalItems(order) }}</td>
              <td class="px-6 py-3.5 text-right text-[0.82rem] font-medium" style="color: var(--admin-text-primary);">{{ orderTotal(order) }}</td>
              <td class="px-6 py-3.5">
                <div class="flex justify-center">
                  <StatusBadge :status="STATUS_MAP[order.status] ?? 'pendiente'" />
                </div>
              </td>
              <td class="px-6 py-3.5 text-right text-[0.75rem]" style="color: var(--admin-text-secondary);">{{ formatDate(order.created_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Low stock alert -->
    <div v-if="!store.loading && store.lowStockCount > 0" class="bg-white rounded-xl overflow-hidden" style="box-shadow: var(--admin-card-shadow);">
      <div class="px-6 py-4 flex items-center justify-between" style="border-bottom: 1px solid var(--admin-border);">
        <p class="text-[0.75rem] font-semibold uppercase tracking-wider" style="color: var(--status-warn-text);">
          ⚠ Stock Bajo ({{ store.lowStockCount }} variantes)
        </p>
        <RouterLink to="/admin/inventory" class="text-[0.72rem] font-medium" style="color: var(--admin-amber);">
          Ver inventario →
        </RouterLink>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr style="background: var(--admin-bg);">
              <th class="px-6 py-2.5 text-left font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">SKU</th>
              <th class="px-6 py-2.5 text-left font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Talla · Color</th>
              <th class="px-6 py-2.5 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Stock</th>
            </tr>
          </thead>
          <tbody class="divide-y" style="border-color: var(--admin-border);">
            <tr v-for="v in store.lowStock" :key="v.id">
              <td class="px-6 py-3 font-mono text-[0.72rem]" style="color: var(--admin-text-secondary);">{{ v.sku }}</td>
              <td class="px-6 py-3 text-[0.78rem]" style="color: var(--admin-text-primary);">{{ v.size }} · {{ v.color }}</td>
              <td class="px-6 py-3 text-right text-[0.82rem] font-bold" style="color: var(--status-warn-text);">{{ v.stock_qty }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>
