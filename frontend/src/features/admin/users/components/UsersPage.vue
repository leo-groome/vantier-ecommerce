<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminStatCard from '@features/admin/components/shared/AdminStatCard.vue'
import AdminFilterBar from '@features/admin/components/shared/AdminFilterBar.vue'
import StatusBadge from '@features/admin/components/shared/StatusBadge.vue'
import type { AdminStatus } from '@features/admin/components/shared/StatusBadge.vue'

type UserRole = 'owner' | 'admin' | 'customer'

interface User {
  id: string
  name: string
  email: string
  role: UserRole
  orders: number
  totalSpent: number
  joinedAt: string
  active: boolean
}

const users = ref<User[]>([])
const loading = ref(true)
const search = ref('')
const roleFilter = ref<UserRole | 'all'>('all')

const filtered = computed(() => {
  let list = users.value
  if (roleFilter.value !== 'all') list = list.filter(u => u.role === roleFilter.value)
  if (search.value) {
    const q = search.value.toLowerCase()
    list = list.filter(u => u.name.toLowerCase().includes(q) || u.email.toLowerCase().includes(q))
  }
  return list
})

const counts = computed(() => ({
  all: users.value.length,
  owner: users.value.filter(u => u.role === 'owner').length,
  admin: users.value.filter(u => u.role === 'admin').length,
  customer: users.value.filter(u => u.role === 'customer').length,
}))

function roleStatus(role: UserRole): AdminStatus {
  if (role === 'owner') return 'activo'
  return 'ok'
}

onMounted(() => {
  setTimeout(() => {
    users.value = [
      { id: 'u1', name: 'Ricardo V.',      email: 'owner@vantierluxuryla.com', role: 'owner',    orders: 0,  totalSpent: 0,     joinedAt: 'Jan 1, 2024',  active: true  },
      { id: 'u2', name: 'Sofia Admin',     email: 'sofia@vantier.com',          role: 'admin',    orders: 0,  totalSpent: 0,     joinedAt: 'Jan 15, 2024', active: true  },
      { id: 'u3', name: 'Carlos Mendoza',  email: 'carlos@example.com',         role: 'customer', orders: 8,  totalSpent: 1440,  joinedAt: 'Feb 3, 2024',  active: true  },
      { id: 'u4', name: 'Andrés Fuentes',  email: 'andres@example.com',         role: 'customer', orders: 3,  totalSpent: 660,   joinedAt: 'Feb 14, 2024', active: true  },
      { id: 'u5', name: 'Miguel Torres',   email: 'miguel@example.com',         role: 'customer', orders: 12, totalSpent: 2280,  joinedAt: 'Jan 28, 2024', active: true  },
      { id: 'u6', name: 'Ricardo Salinas', email: 'ricardo@example.com',        role: 'customer', orders: 5,  totalSpent: 950,   joinedAt: 'Mar 2, 2024',  active: true  },
      { id: 'u7', name: 'Javier Ríos',     email: 'javier@example.com',         role: 'customer', orders: 2,  totalSpent: 390,   joinedAt: 'Mar 18, 2024', active: true  },
      { id: 'u8', name: 'Luis Herrera',    email: 'luis@example.com',           role: 'customer', orders: 1,  totalSpent: 220,   joinedAt: 'Apr 1, 2024',  active: false },
      { id: 'u9', name: 'Fernando López',  email: 'fernando@example.com',       role: 'customer', orders: 15, totalSpent: 3150,  joinedAt: 'Jan 10, 2024', active: true  },
    ]
    loading.value = false
  }, 400)
})
</script>

<template>
  <div class="space-y-6">


    <!-- Stats -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <AdminStatCard label="Total" :value="String(counts.all)" icon="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
      <AdminStatCard label="Owners" :value="String(counts.owner)" icon="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
      <AdminStatCard label="Admins" :value="String(counts.admin)" icon="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
      <AdminStatCard label="Clientes" :value="String(counts.customer)" icon="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
    </div>

    <!-- Table Card -->
    <div class="bg-white rounded-xl overflow-hidden" style="box-shadow: var(--admin-card-shadow);">
      <!-- Filters -->
      <div class="px-6 py-4 border-b flex flex-col md:flex-row md:items-center justify-between gap-4" style="border-color: var(--admin-border);">
        <p class="text-[0.72rem] font-semibold uppercase tracking-wider" style="color: var(--admin-text-primary);">Lista de Usuarios</p>
        <AdminFilterBar v-model="search" placeholder="Buscar por nombre o email…">
          <select
            v-model="roleFilter"
            class="h-8 px-3 text-[0.75rem] rounded-lg appearance-none cursor-pointer focus:outline-none bg-white border"
            style="border-color: rgba(0,0,0,0.1); color: var(--admin-text-primary);"
          >
            <option value="all">Todos los roles</option>
            <option value="owner">Owner</option>
            <option value="admin">Admin</option>
            <option value="customer">Customer</option>
          </select>
        </AdminFilterBar>
      </div>

      <!-- Skeleton -->
      <div v-if="loading" class="p-6 space-y-4">
        <div v-for="i in 5" :key="i" class="h-12 rounded-lg animate-pulse" style="background: rgba(0,0,0,0.06);" />
      </div>

      <!-- Table -->
      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr style="background: var(--admin-bg);">
              <th class="px-6 py-3 text-left font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Usuario / Email</th>
              <th class="px-6 py-3 text-center font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Rol</th>
              <th class="px-6 py-3 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Órdenes</th>
              <th class="px-6 py-3 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Inversión</th>
              <th class="px-6 py-3 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Registro</th>
              <th class="px-6 py-3 text-center font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Estado</th>
            </tr>
          </thead>
          <tbody class="divide-y" style="border-color: var(--admin-border);">
            <tr
              v-for="user in filtered"
              :key="user.id"
              class="hover:bg-black/[0.01] transition-colors"
            >
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div
                    class="w-8 h-8 rounded-full flex items-center justify-center text-[0.7rem] font-bold text-white flex-shrink-0"
                    style="background: linear-gradient(135deg, var(--admin-amber), #a07820);"
                  >
                    {{ user.name.charAt(0) }}
                  </div>
                  <div>
                    <p class="text-[0.82rem] font-bold" style="color: var(--admin-text-primary);">{{ user.name }}</p>
                    <p class="text-[0.72rem]" style="color: var(--admin-text-secondary);">{{ user.email }}</p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="flex justify-center">
                  <StatusBadge :status="user.role as any" />
                </div>
              </td>
              <td class="px-6 py-4 text-right text-[0.82rem]" style="color: var(--admin-text-secondary);">{{ user.orders }}</td>
              <td class="px-6 py-4 text-right text-[0.82rem] font-bold" style="color: var(--admin-text-primary);">
                {{ user.totalSpent > 0 ? `$${user.totalSpent.toLocaleString()}` : '—' }}
              </td>
              <td class="px-6 py-4 text-right text-[0.72rem]" style="color: var(--admin-text-secondary);">{{ user.joinedAt }}</td>
              <td class="px-6 py-4">
                <div class="flex justify-center">
                  <StatusBadge :status="user.active ? 'activo' : 'inactivo'" />
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
