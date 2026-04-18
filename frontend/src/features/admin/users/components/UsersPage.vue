<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminStatCard from '@features/admin/components/shared/AdminStatCard.vue'
import AdminFilterBar from '@features/admin/components/shared/AdminFilterBar.vue'
import AdminButton from '@features/admin/components/shared/AdminButton.vue'
import StatusBadge from '@features/admin/components/shared/StatusBadge.vue'
import { useAdminUsersStore } from '../store'
import type { AdminRole } from '../types'

const store = useAdminUsersStore()

const search = ref('')
const showInvite = ref(false)
const removingId = ref<string | null>(null)

const inviteForm = ref({ email: '', role: 'operative' as AdminRole })
const inviteError = ref('')
const inviting = ref(false)

function resetInviteForm() {
  inviteForm.value = { email: '', role: 'operative' }
  inviteError.value = ''
}

const filtered = computed(() => {
  if (!search.value) return store.users
  const q = search.value.toLowerCase()
  return store.users.filter(u => u.email.toLowerCase().includes(q))
})

const counts = computed(() => ({
  total: store.users.length,
  owner: store.users.filter(u => u.role === 'owner').length,
  operative: store.users.filter(u => u.role === 'operative').length,
  active: store.users.filter(u => u.is_active).length,
}))

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('es-MX', { day: 'numeric', month: 'short', year: 'numeric' })
}

async function sendInvite() {
  if (!inviteForm.value.email.trim()) { inviteError.value = 'El email es requerido'; return }
  inviting.value = true
  inviteError.value = ''
  const result = await store.invite({ email: inviteForm.value.email.trim(), role: inviteForm.value.role })
  inviting.value = false
  if (result) {
    showInvite.value = false
    resetInviteForm()
  } else {
    inviteError.value = store.error ?? 'Error al invitar usuario'
  }
}

async function changeRole(id: string, role: AdminRole) {
  await store.changeRole(id, role)
}

async function removeUser(id: string) {
  removingId.value = id
  await store.deactivate(id)
  removingId.value = null
}

onMounted(() => store.loadUsers())
</script>

<template>
  <div class="space-y-6">

    <!-- Stats -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <AdminStatCard
        label="Total Staff"
        :value="String(counts.total)"
        icon="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
      />
      <AdminStatCard
        label="Owners"
        :value="String(counts.owner)"
        icon="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
      />
      <AdminStatCard
        label="Operativos"
        :value="String(counts.operative)"
        icon="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
      />
      <AdminStatCard
        label="Activos"
        :value="String(counts.active)"
        icon="M5 13l4 4L19 7"
      />
    </div>

    <!-- Actions -->
    <div class="flex items-center justify-between gap-4 flex-wrap">
      <p class="text-[0.72rem] font-semibold uppercase tracking-wider" style="color: var(--admin-text-secondary);">Equipo administrativo</p>
      <AdminButton variant="primary" @click="showInvite = true">
        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        Invitar Usuario
      </AdminButton>
    </div>

    <!-- Error -->
    <div v-if="store.error" class="text-[0.82rem] text-red-600 px-1">{{ store.error }}</div>

    <!-- Table Card -->
    <div class="bg-white rounded-xl overflow-hidden" style="box-shadow: var(--admin-card-shadow);">
      <!-- Search -->
      <div class="px-6 py-4 border-b" style="border-color: var(--admin-border);">
        <AdminFilterBar v-model="search" placeholder="Buscar por email…" />
      </div>

      <!-- Skeleton -->
      <div v-if="store.loading" class="p-6 space-y-4">
        <div v-for="i in 3" :key="i" class="h-12 rounded-lg animate-pulse" style="background: rgba(0,0,0,0.06);" />
      </div>

      <!-- Empty -->
      <div v-else-if="filtered.length === 0" class="py-12 text-center text-[0.85rem]" style="color: var(--admin-text-secondary);">
        Sin usuarios{{ search ? ' con esa búsqueda' : '' }}.
      </div>

      <!-- Table -->
      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr style="background: var(--admin-bg);">
              <th class="px-6 py-3 text-left font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Email</th>
              <th class="px-6 py-3 text-center font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Rol</th>
              <th class="px-6 py-3 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Creado</th>
              <th class="px-6 py-3 text-center font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Estado</th>
              <th class="px-6 py-3 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y" style="border-color: var(--admin-border);">
            <tr
              v-for="user in filtered"
              :key="user.id"
              class="hover:bg-black/[0.01] transition-colors"
              :class="{ 'opacity-50': !user.is_active }"
            >
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div
                    class="w-8 h-8 rounded-full flex items-center justify-center text-[0.7rem] font-bold text-white flex-shrink-0"
                    style="background: linear-gradient(135deg, var(--admin-amber), #a07820);"
                  >
                    {{ user.email.charAt(0).toUpperCase() }}
                  </div>
                  <p class="text-[0.82rem]" style="color: var(--admin-text-primary);">{{ user.email }}</p>
                </div>
              </td>
              <td class="px-6 py-4 text-center">
                <select
                  :value="user.role"
                  class="text-[0.75rem] border rounded-lg px-2 py-1 bg-white focus:outline-none cursor-pointer"
                  style="border-color: rgba(0,0,0,0.12); color: var(--admin-text-primary);"
                  :disabled="!user.is_active"
                  @change="changeRole(user.id, ($event.target as HTMLSelectElement).value as AdminRole)"
                >
                  <option value="owner">Owner</option>
                  <option value="operative">Operative</option>
                </select>
              </td>
              <td class="px-6 py-4 text-right text-[0.72rem]" style="color: var(--admin-text-secondary);">{{ formatDate(user.created_at) }}</td>
              <td class="px-6 py-4 text-center">
                <StatusBadge :status="user.is_active ? 'activo' : 'inactivo'" />
              </td>
              <td class="px-6 py-4 text-right">
                <button
                  v-if="user.is_active"
                  class="text-[0.7rem] uppercase font-bold tracking-widest text-red-500 px-2 py-1 rounded hover:bg-red-50 transition-colors disabled:opacity-40"
                  :disabled="removingId === user.id"
                  @click="removeUser(user.id)"
                >
                  <span v-if="removingId === user.id" class="inline-block w-3 h-3 border border-current border-t-transparent rounded-full animate-spin" />
                  <span v-else>Remover</span>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Invite modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showInvite" class="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="showInvite = false; resetInviteForm()" />
          <div class="relative w-full max-w-sm bg-white rounded-2xl shadow-2xl p-6 space-y-5">
            <div class="flex items-center justify-between">
              <h2 class="text-[0.9rem] font-semibold" style="color: var(--admin-text-primary);">Invitar Usuario</h2>
              <button style="color: var(--admin-text-secondary);" @click="showInvite = false; resetInviteForm()">✕</button>
            </div>

            <div class="space-y-4">
              <div>
                <label class="text-[0.65rem] uppercase tracking-wider block mb-1.5" style="color: var(--admin-text-secondary);">Email</label>
                <input
                  v-model="inviteForm.email"
                  type="email"
                  placeholder="usuario@empresa.com"
                  class="w-full border rounded-lg px-3 py-2 text-[0.82rem] focus:outline-none"
                  style="border-color: rgba(0,0,0,0.12); color: var(--admin-text-primary);"
                />
              </div>
              <div>
                <label class="text-[0.65rem] uppercase tracking-wider block mb-1.5" style="color: var(--admin-text-secondary);">Rol</label>
                <select
                  v-model="inviteForm.role"
                  class="w-full border rounded-lg px-3 py-2 text-[0.82rem] bg-white focus:outline-none"
                  style="border-color: rgba(0,0,0,0.12); color: var(--admin-text-primary);"
                >
                  <option value="operative">Operative</option>
                  <option value="owner">Owner</option>
                </select>
              </div>
              <p v-if="inviteError" class="text-[0.72rem] text-red-600">{{ inviteError }}</p>
            </div>

            <div class="flex justify-end gap-3 pt-1">
              <button
                class="text-[0.75rem] px-4 py-2"
                style="color: var(--admin-text-secondary);"
                @click="showInvite = false; resetInviteForm()"
              >Cancelar</button>
              <AdminButton variant="primary" :loading="inviting" @click="sendInvite">
                Invitar
              </AdminButton>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.modal-enter-active { transition: opacity 0.15s ease; }
.modal-leave-active { transition: opacity 0.1s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
</style>
