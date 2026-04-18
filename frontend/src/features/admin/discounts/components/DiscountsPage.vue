<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AdminButton from '@features/admin/components/shared/AdminButton.vue'
import StatusBadge from '@features/admin/components/shared/StatusBadge.vue'
import { useAdminDiscountsStore } from '../store'

const store = useAdminDiscountsStore()

const showCreate = ref(false)
const togglingId = ref<string | null>(null)

const form = ref({
  code: '',
  type: 'percent' as 'percent' | 'fixed',
  value: 10,
  maxUsage: '' as number | '',
  expiresAt: '',
})
const createError = ref('')
const creating = ref(false)

function resetForm() {
  form.value = { code: '', type: 'percent', value: 10, maxUsage: '', expiresAt: '' }
  createError.value = ''
}

async function createDiscount() {
  if (!form.value.code.trim()) { createError.value = 'El código es requerido'; return }
  if (form.value.value <= 0) { createError.value = 'El valor debe ser mayor a 0'; return }
  creating.value = true
  createError.value = ''
  const result = await store.addDiscount({
    code: form.value.code.toUpperCase().trim(),
    type: form.value.type,
    value: form.value.value,
    usage_limit: form.value.maxUsage === '' ? undefined : Number(form.value.maxUsage),
    expires_at: form.value.expiresAt || undefined,
  })
  creating.value = false
  if (result) {
    showCreate.value = false
    resetForm()
  } else {
    createError.value = store.error ?? 'Error al crear descuento'
  }
}

async function toggleActive(id: string, currentState: boolean) {
  togglingId.value = id
  await store.editDiscount(id, { is_active: !currentState })
  togglingId.value = null
}

onMounted(() => store.loadDiscounts())
</script>

<template>
  <div class="space-y-6">
    <!-- Actions -->
    <div class="flex justify-end">
      <AdminButton variant="primary" @click="showCreate = true">
        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        Nuevo Código
      </AdminButton>
    </div>

    <!-- Error -->
    <div v-if="store.error" class="text-[0.82rem] text-red-600 px-1">{{ store.error }}</div>

    <!-- Skeleton -->
    <div v-if="store.loading" class="space-y-3">
      <div v-for="i in 4" :key="i" class="h-14 rounded-xl animate-pulse" style="background: rgba(0,0,0,0.06);" />
    </div>

    <!-- Empty -->
    <div v-else-if="!store.loading && store.discounts.length === 0" class="py-12 text-center text-[0.85rem]" style="color: var(--admin-text-secondary);">
      Sin códigos de descuento. Crea el primero.
    </div>

    <!-- Table -->
    <div v-else class="bg-white rounded-xl overflow-hidden" style="box-shadow: var(--admin-card-shadow);">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr style="background: var(--admin-bg);">
              <th class="px-6 py-3 text-left font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Código</th>
              <th class="px-6 py-3 text-left font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Descuento</th>
              <th class="px-6 py-3 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Uso</th>
              <th class="px-6 py-3 text-left font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Expira</th>
              <th class="px-6 py-3 text-center font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Estado</th>
              <th class="px-6 py-3 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y" style="border-color: var(--admin-border);">
            <tr
              v-for="d in store.discounts"
              :key="d.id"
              class="hover:bg-black/[0.01] transition-colors"
              :class="{ 'opacity-50': !d.is_active }"
            >
              <td class="px-6 py-4">
                <span class="font-mono text-[0.82rem] font-bold p-1 rounded bg-black/5" style="color: var(--admin-text-primary);">{{ d.code }}</span>
              </td>
              <td class="px-6 py-4 text-[0.82rem]" style="color: var(--admin-text-primary);">
                {{ d.type === 'percent' ? `${d.value}% off` : `$${d.value} off` }}
              </td>
              <td class="px-6 py-4 text-right">
                <span class="text-[0.82rem] font-medium" style="color: var(--admin-text-primary);">{{ d.usage_count }}</span>
                <span v-if="d.usage_limit" class="text-[0.72rem]" style="color: var(--admin-text-secondary);"> / {{ d.usage_limit }}</span>
                <span v-if="d.usage_limit && d.usage_count >= d.usage_limit" class="ml-1.5 text-[0.65rem] font-bold uppercase text-red-500">Agotado</span>
              </td>
              <td class="px-6 py-4 text-[0.75rem]" style="color: var(--admin-text-secondary);">
                {{ d.expires_at ? new Date(d.expires_at).toLocaleDateString('es-MX') : '—' }}
              </td>
              <td class="px-6 py-4">
                <div class="flex justify-center">
                  <StatusBadge :status="d.is_active ? 'activo' : 'inactivo'" />
                </div>
              </td>
              <td class="px-6 py-4 text-right">
                <button
                  class="text-[0.7rem] uppercase font-bold tracking-widest px-2 py-1 rounded transition-colors disabled:opacity-40"
                  :style="{ color: d.is_active ? 'var(--admin-text-secondary)' : 'var(--admin-amber)' }"
                  :disabled="togglingId === d.id"
                  @click="toggleActive(d.id, d.is_active)"
                >
                  <span v-if="togglingId === d.id" class="inline-block w-3 h-3 border border-current border-t-transparent rounded-full animate-spin" />
                  <span v-else>{{ d.is_active ? 'Desactivar' : 'Activar' }}</span>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showCreate" class="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="showCreate = false; resetForm()" />
          <div class="relative w-full max-w-md bg-white rounded-2xl shadow-2xl p-6 space-y-5">
            <div class="flex items-center justify-between">
              <h2 class="text-[0.9rem] font-semibold" style="color: var(--admin-text-primary);">Nuevo Código de Descuento</h2>
              <button style="color: var(--admin-text-secondary);" @click="showCreate = false; resetForm()">✕</button>
            </div>

            <div class="space-y-4">
              <!-- Code -->
              <div>
                <label class="text-[0.65rem] uppercase tracking-wider block mb-1.5" style="color: var(--admin-text-secondary);">Código</label>
                <input
                  v-model="form.code"
                  type="text"
                  placeholder="ej. VERANO2024"
                  class="w-full border rounded-lg px-3 py-2 text-[0.82rem] font-mono focus:outline-none"
                  style="border-color: rgba(0,0,0,0.12); color: var(--admin-text-primary);"
                />
              </div>

              <!-- Type + Value -->
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="text-[0.65rem] uppercase tracking-wider block mb-1.5" style="color: var(--admin-text-secondary);">Tipo</label>
                  <select
                    v-model="form.type"
                    class="w-full border rounded-lg px-3 py-2 text-[0.82rem] bg-white focus:outline-none"
                    style="border-color: rgba(0,0,0,0.12); color: var(--admin-text-primary);"
                  >
                    <option value="percent">Porcentaje (%)</option>
                    <option value="fixed">Fijo ($)</option>
                  </select>
                </div>
                <div>
                  <label class="text-[0.65rem] uppercase tracking-wider block mb-1.5" style="color: var(--admin-text-secondary);">Valor</label>
                  <input
                    v-model.number="form.value"
                    type="number"
                    min="1"
                    class="w-full border rounded-lg px-3 py-2 text-[0.82rem] focus:outline-none"
                    style="border-color: rgba(0,0,0,0.12); color: var(--admin-text-primary);"
                  />
                </div>
              </div>

              <!-- Max Usage + Expiry -->
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="text-[0.65rem] uppercase tracking-wider block mb-1.5" style="color: var(--admin-text-secondary);">Usos Máx. (vacío = ∞)</label>
                  <input
                    v-model="form.maxUsage"
                    type="number"
                    min="1"
                    placeholder="∞"
                    class="w-full border rounded-lg px-3 py-2 text-[0.82rem] focus:outline-none"
                    style="border-color: rgba(0,0,0,0.12); color: var(--admin-text-primary);"
                  />
                </div>
                <div>
                  <label class="text-[0.65rem] uppercase tracking-wider block mb-1.5" style="color: var(--admin-text-secondary);">Expira el (opcional)</label>
                  <input
                    v-model="form.expiresAt"
                    type="date"
                    class="w-full border rounded-lg px-3 py-2 text-[0.82rem] focus:outline-none"
                    style="border-color: rgba(0,0,0,0.12); color: var(--admin-text-primary);"
                  />
                </div>
              </div>

              <p v-if="createError" class="text-[0.72rem] text-red-600">{{ createError }}</p>
            </div>

            <div class="flex justify-end gap-3 pt-1">
              <button
                class="text-[0.75rem] px-4 py-2"
                style="color: var(--admin-text-secondary);"
                @click="showCreate = false; resetForm()"
              >Cancelar</button>
              <AdminButton variant="primary" :loading="creating" @click="createDiscount">
                Crear Descuento
              </AdminButton>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.modal-enter-active { transition: opacity 0.15s ease, transform 0.15s ease; }
.modal-leave-active { transition: opacity 0.1s ease, transform 0.1s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
</style>
