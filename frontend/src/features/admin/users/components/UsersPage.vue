<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

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

const ROLE_COLORS: Record<UserRole, string> = {
  owner:    'text-purple-700 bg-purple-50 border-purple-200',
  admin:    'text-blue-700 bg-blue-50 border-blue-200',
  customer: 'text-[color:var(--color-border-strong)] bg-[color:var(--color-warm-beige)] border-[color:var(--color-border)]',
}

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
    <!-- Header -->
    <div>
      <p class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)]">Access</p>
      <h1 class="mt-1 text-2xl font-semibold uppercase tracking-wider text-[color:var(--color-obsidian)]">Users</h1>
    </div>

    <!-- Controls -->
    <div class="flex flex-wrap items-center gap-3">
      <!-- Search -->
      <div class="relative">
        <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[color:var(--color-border-strong)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35" stroke-linecap="round"/>
        </svg>
        <input
          v-model="search"
          type="text"
          placeholder="Search users…"
          class="pl-9 pr-4 py-2 text-sm border border-[color:var(--color-border)] rounded-[var(--radius-md)] bg-[color:var(--color-ivory)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors"
        />
      </div>

      <!-- Role tabs -->
      <div class="flex gap-1.5">
        <button
          v-for="r in ['all', 'owner', 'admin', 'customer']"
          :key="r"
          class="flex items-center gap-1.5 px-3 py-1.5 text-xs uppercase tracking-widest rounded-[var(--radius-md)] border transition-colors duration-[var(--duration-fast)]"
          :class="roleFilter === r
            ? 'bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] border-[color:var(--color-obsidian)]'
            : 'border-[color:var(--color-border)] text-[color:var(--color-border-strong)] hover:border-[color:var(--color-obsidian)] hover:text-[color:var(--color-obsidian)]'"
          @click="roleFilter = r as any"
        >
          {{ r }}
          <span class="font-semibold">{{ counts[r as keyof typeof counts] ?? 0 }}</span>
        </button>
      </div>
    </div>

    <!-- Skeleton -->
    <div v-if="loading" class="space-y-3">
      <div v-for="i in 5" :key="i" class="h-16 rounded-[var(--radius-md)] bg-[color:var(--color-warm-beige-dk)] animate-pulse" />
    </div>

    <!-- Table -->
    <div v-else class="bg-[color:var(--color-ivory)] border border-[color:var(--color-border)] rounded-[var(--radius-md)] overflow-hidden">
      <div v-if="filtered.length === 0" class="py-12 text-center text-sm text-[color:var(--color-border-strong)]">
        No users found.
      </div>
      <table v-else class="w-full text-sm">
        <thead>
          <tr class="bg-[color:var(--color-warm-beige)] text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] border-b border-[color:var(--color-border)]">
            <th class="px-5 py-3 text-left font-medium">User</th>
            <th class="px-5 py-3 text-center font-medium">Role</th>
            <th class="px-5 py-3 text-right font-medium">Orders</th>
            <th class="px-5 py-3 text-right font-medium">Total Spent</th>
            <th class="px-5 py-3 text-right font-medium">Joined</th>
            <th class="px-5 py-3 text-center font-medium">Status</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-[color:var(--color-border)]">
          <tr
            v-for="user in filtered"
            :key="user.id"
            class="hover:bg-[color:var(--color-warm-beige)] transition-colors duration-[var(--duration-fast)]"
          >
            <td class="px-5 py-3.5">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full bg-[color:var(--color-obsidian)] flex items-center justify-center text-[color:var(--color-ivory)] text-xs font-bold flex-shrink-0">
                  {{ user.name.charAt(0) }}
                </div>
                <div>
                  <p class="font-medium text-[color:var(--color-obsidian)]">{{ user.name }}</p>
                  <p class="text-xs text-[color:var(--color-border-strong)]">{{ user.email }}</p>
                </div>
              </div>
            </td>
            <td class="px-5 py-3.5">
              <div class="flex justify-center">
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium uppercase tracking-wider border"
                  :class="ROLE_COLORS[user.role]"
                >{{ user.role }}</span>
              </div>
            </td>
            <td class="px-5 py-3.5 text-right text-[color:var(--color-border-strong)]">{{ user.orders }}</td>
            <td class="px-5 py-3.5 text-right font-medium text-[color:var(--color-obsidian)]">
              {{ user.totalSpent > 0 ? `$${user.totalSpent.toLocaleString()}` : '—' }}
            </td>
            <td class="px-5 py-3.5 text-right text-xs text-[color:var(--color-border-strong)]">{{ user.joinedAt }}</td>
            <td class="px-5 py-3.5">
              <div class="flex justify-center">
                <span
                  class="inline-flex items-center gap-1 text-xs"
                  :class="user.active ? 'text-emerald-600' : 'text-[color:var(--color-border-strong)]'"
                >
                  <span class="w-1.5 h-1.5 rounded-full" :class="user.active ? 'bg-emerald-500' : 'bg-[color:var(--color-border)]'" />
                  {{ user.active ? 'Active' : 'Inactive' }}
                </span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
