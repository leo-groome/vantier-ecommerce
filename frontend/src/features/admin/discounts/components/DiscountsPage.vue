<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Discount {
  id: string
  code: string
  type: 'percentage' | 'fixed'
  value: number
  minItems: number
  usageCount: number
  maxUsage: number | null
  active: boolean
  expiresAt: string | null
}

const discounts = ref<Discount[]>([])
const loading = ref(true)
const showCreate = ref(false)
const deletingId = ref<string | null>(null)
const togglingId = ref<string | null>(null)

// Create form state
const form = ref({
  code: '',
  type: 'percentage' as 'percentage' | 'fixed',
  value: 10,
  minItems: 1,
  maxUsage: '' as number | '',
  expiresAt: '',
})
const createError = ref('')
const creating = ref(false)

function resetForm() {
  form.value = { code: '', type: 'percentage', value: 10, minItems: 1, maxUsage: '', expiresAt: '' }
  createError.value = ''
}

async function createDiscount() {
  if (!form.value.code.trim()) { createError.value = 'Code is required'; return }
  if (form.value.value <= 0) { createError.value = 'Value must be > 0'; return }
  creating.value = true
  await new Promise(r => setTimeout(r, 500))
  discounts.value.unshift({
    id: Date.now().toString(),
    code: form.value.code.toUpperCase().trim(),
    type: form.value.type,
    value: form.value.value,
    minItems: form.value.minItems,
    usageCount: 0,
    maxUsage: form.value.maxUsage === '' ? null : Number(form.value.maxUsage),
    active: true,
    expiresAt: form.value.expiresAt || null,
  })
  creating.value = false
  showCreate.value = false
  resetForm()
}

async function toggleActive(d: Discount) {
  togglingId.value = d.id
  await new Promise(r => setTimeout(r, 300))
  d.active = !d.active
  togglingId.value = null
}

async function deleteDiscount(id: string) {
  deletingId.value = id
  await new Promise(r => setTimeout(r, 400))
  discounts.value = discounts.value.filter(d => d.id !== id)
  deletingId.value = null
}

onMounted(() => {
  setTimeout(() => {
    discounts.value = [
      { id: '1', code: 'VANTIER10',   type: 'percentage', value: 10, minItems: 1, usageCount: 42,  maxUsage: null, active: true,  expiresAt: null },
      { id: '2', code: 'WELCOME20',   type: 'percentage', value: 20, minItems: 1, usageCount: 18,  maxUsage: 50,   active: true,  expiresAt: '2024-06-30' },
      { id: '3', code: 'BUNDLE5',     type: 'fixed',      value: 25, minItems: 5, usageCount: 7,   maxUsage: null, active: true,  expiresAt: null },
      { id: '4', code: 'SPRING2024',  type: 'percentage', value: 15, minItems: 2, usageCount: 100, maxUsage: 100,  active: false, expiresAt: '2024-04-01' },
    ]
    loading.value = false
  }, 400)
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-end justify-between gap-4">
      <div>
        <p class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)]">Promotions</p>
        <h1 class="mt-1 text-2xl font-semibold uppercase tracking-wider text-[color:var(--color-obsidian)]">Discounts</h1>
      </div>
      <button
        class="flex items-center gap-2 px-4 py-2.5 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-xs uppercase tracking-widest rounded-[var(--radius-md)] hover:opacity-80 transition-opacity duration-[var(--duration-fast)]"
        @click="showCreate = true"
      >
        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        New Code
      </button>
    </div>

    <!-- Skeleton -->
    <div v-if="loading" class="space-y-3">
      <div v-for="i in 4" :key="i" class="h-16 rounded-[var(--radius-md)] bg-[color:var(--color-warm-beige-dk)] animate-pulse" />
    </div>

    <!-- Table -->
    <div v-else class="bg-[color:var(--color-ivory)] border border-[color:var(--color-border)] rounded-[var(--radius-md)] overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="bg-[color:var(--color-warm-beige)] text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] border-b border-[color:var(--color-border)]">
            <th class="px-5 py-3 text-left font-medium">Code</th>
            <th class="px-5 py-3 text-left font-medium">Discount</th>
            <th class="px-5 py-3 text-right font-medium">Min Items</th>
            <th class="px-5 py-3 text-right font-medium">Usage</th>
            <th class="px-5 py-3 text-left font-medium">Expires</th>
            <th class="px-5 py-3 text-center font-medium">Active</th>
            <th class="px-5 py-3 text-right font-medium">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-[color:var(--color-border)]">
          <tr
            v-for="d in discounts"
            :key="d.id"
            class="hover:bg-[color:var(--color-warm-beige)] transition-colors duration-[var(--duration-fast)]"
            :class="{ 'opacity-50': !d.active }"
          >
            <td class="px-5 py-3.5">
              <span class="font-mono text-sm font-medium text-[color:var(--color-obsidian)] bg-[color:var(--color-warm-beige)] px-2 py-0.5 rounded-[var(--radius-sm)]">{{ d.code }}</span>
            </td>
            <td class="px-5 py-3.5 text-[color:var(--color-obsidian)]">
              {{ d.type === 'percentage' ? `${d.value}% off` : `$${d.value} off` }}
            </td>
            <td class="px-5 py-3.5 text-right text-[color:var(--color-border-strong)]">{{ d.minItems }}</td>
            <td class="px-5 py-3.5 text-right">
              <span class="text-[color:var(--color-obsidian)]">{{ d.usageCount }}</span>
              <span v-if="d.maxUsage" class="text-[color:var(--color-border-strong)]"> / {{ d.maxUsage }}</span>
              <span v-if="d.maxUsage && d.usageCount >= d.maxUsage" class="ml-1.5 text-xs text-red-500">Exhausted</span>
            </td>
            <td class="px-5 py-3.5 text-sm text-[color:var(--color-border-strong)]">
              {{ d.expiresAt ?? '—' }}
            </td>
            <td class="px-5 py-3.5">
              <div class="flex justify-center">
                <button
                  class="w-10 h-5 rounded-full transition-colors duration-[var(--duration-normal)] relative flex-shrink-0"
                  :class="d.active ? 'bg-[color:var(--color-obsidian)]' : 'bg-[color:var(--color-border)]'"
                  :disabled="togglingId === d.id"
                  :aria-label="d.active ? 'Deactivate' : 'Activate'"
                  @click="toggleActive(d)"
                >
                  <span
                    class="absolute top-0.5 w-4 h-4 rounded-full bg-white shadow-sm transition-transform duration-[var(--duration-normal)]"
                    :class="d.active ? 'translate-x-5' : 'translate-x-0.5'"
                  />
                </button>
              </div>
            </td>
            <td class="px-5 py-3.5 text-right">
              <button
                class="text-xs text-red-500 hover:text-red-700 uppercase tracking-wider transition-colors disabled:opacity-40"
                :disabled="deletingId === d.id"
                @click="deleteDiscount(d.id)"
              >
                <span v-if="deletingId === d.id" class="inline-block w-3 h-3 border border-current border-t-transparent rounded-full animate-spin" />
                <span v-else>Delete</span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create modal -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div v-if="showCreate" class="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="showCreate = false; resetForm()" />
          <div class="relative w-full max-w-md bg-[color:var(--color-ivory)] rounded-[var(--radius-md)] shadow-2xl overflow-hidden">
            <div class="px-6 py-4 border-b border-[color:var(--color-border)] flex items-center justify-between">
              <p class="text-xs uppercase tracking-widest font-semibold text-[color:var(--color-obsidian)]">New Discount Code</p>
              <button class="p-1.5 hover:opacity-70 transition-opacity" @click="showCreate = false; resetForm()">
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>

            <div class="px-6 py-5 space-y-4">
              <!-- Code -->
              <div>
                <label class="block text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] mb-1.5">Code</label>
                <input
                  v-model="form.code"
                  type="text"
                  placeholder="e.g. SUMMER25"
                  class="w-full border border-[color:var(--color-border)] rounded-[var(--radius-md)] px-3 py-2 text-sm font-mono uppercase focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors"
                />
              </div>

              <!-- Type + Value -->
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] mb-1.5">Type</label>
                  <select
                    v-model="form.type"
                    class="w-full border border-[color:var(--color-border)] rounded-[var(--radius-md)] px-3 py-2 text-sm bg-[color:var(--color-ivory)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors"
                  >
                    <option value="percentage">Percentage (%)</option>
                    <option value="fixed">Fixed ($)</option>
                  </select>
                </div>
                <div>
                  <label class="block text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] mb-1.5">Value</label>
                  <input
                    v-model.number="form.value"
                    type="number"
                    min="1"
                    class="w-full border border-[color:var(--color-border)] rounded-[var(--radius-md)] px-3 py-2 text-sm focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors"
                  />
                </div>
              </div>

              <!-- Min Items + Max Usage -->
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] mb-1.5">Min Items</label>
                  <input
                    v-model.number="form.minItems"
                    type="number"
                    min="1"
                    class="w-full border border-[color:var(--color-border)] rounded-[var(--radius-md)] px-3 py-2 text-sm focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors"
                  />
                </div>
                <div>
                  <label class="block text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] mb-1.5">Max Uses (blank = unlimited)</label>
                  <input
                    v-model="form.maxUsage"
                    type="number"
                    min="1"
                    placeholder="∞"
                    class="w-full border border-[color:var(--color-border)] rounded-[var(--radius-md)] px-3 py-2 text-sm focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors"
                  />
                </div>
              </div>

              <!-- Expires -->
              <div>
                <label class="block text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] mb-1.5">Expires At (optional)</label>
                <input
                  v-model="form.expiresAt"
                  type="date"
                  class="w-full border border-[color:var(--color-border)] rounded-[var(--radius-md)] px-3 py-2 text-sm bg-[color:var(--color-ivory)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors"
                />
              </div>

              <!-- Error -->
              <p v-if="createError" class="text-xs text-red-600">{{ createError }}</p>
            </div>

            <div class="px-6 py-4 border-t border-[color:var(--color-border)] flex items-center justify-end gap-3">
              <button
                class="px-4 py-2 text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] hover:text-[color:var(--color-obsidian)] transition-colors"
                @click="showCreate = false; resetForm()"
              >Cancel</button>
              <button
                class="flex items-center gap-2 px-4 py-2 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-xs uppercase tracking-widest rounded-[var(--radius-md)] hover:opacity-80 transition-opacity disabled:opacity-50"
                :disabled="creating"
                @click="createDiscount"
              >
                <span v-if="creating" class="w-3 h-3 border border-current border-t-transparent rounded-full animate-spin" />
                Create
              </button>
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
