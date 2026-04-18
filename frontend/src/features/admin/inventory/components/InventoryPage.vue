<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAdminInventoryStore } from '../store'
import { LINE_LABELS, STYLE_LABELS } from '@features/products/types'
import type { AdminProduct, AdminVariant, ProductCreatePayload, VariantCreatePayload, ProductLine, ProductStyle, ProductSize } from '../types'
import { uploadVariantImage } from '../api'
import AdminStatCard from '@features/admin/components/shared/AdminStatCard.vue'
import StatusBadge from '@features/admin/components/shared/StatusBadge.vue'
import StockBar from '@features/admin/components/shared/StockBar.vue'
import AdminButton from '@features/admin/components/shared/AdminButton.vue'
import AdminFilterBar from '@features/admin/components/shared/AdminFilterBar.vue'
import type { AdminStatus } from '@features/admin/components/shared/StatusBadge.vue'

const store = useAdminInventoryStore()

const search      = ref('')
const lineFilter  = ref('all')
const stockFilter = ref('all')
const saving      = ref<string | null>(null)
const showAddProduct = ref(false)
const showAddVariant = ref<string | null>(null)
const showImages     = ref<{ productId: string; variant: AdminVariant } | null>(null)
const imageUploading = ref(false)

// ── Add Product ──────────────────────────────────────────────────────────────
const newProduct = ref<ProductCreatePayload>({ line: 'polo_atelier', name: '', description: '' })
const creatingProduct = ref(false)

async function submitAddProduct() {
  if (!newProduct.value.name.trim()) return
  creatingProduct.value = true
  const product = await store.createProduct({ ...newProduct.value, description: newProduct.value.description || undefined })
  creatingProduct.value = false
  if (product) {
    showAddProduct.value = false
    newProduct.value = { line: 'polo_atelier', name: '', description: '' }
  }
}

// ── Add Variant ──────────────────────────────────────────────────────────────
const newVariant = ref<VariantCreatePayload>({ style: 'classic', size: 'M', color: '', price_usd: 0, cost_acquisition_usd: 0, stock_qty: 0 })
const creatingVariant = ref(false)

async function submitAddVariant(productId: string) {
  if (!newVariant.value.color.trim() || newVariant.value.price_usd <= 0) return
  creatingVariant.value = true
  const ok = await store.addVariant(productId, newVariant.value)
  creatingVariant.value = false
  if (ok) {
    showAddVariant.value = null
    newVariant.value = { style: 'classic', size: 'M', color: '', price_usd: 0, cost_acquisition_usd: 0, stock_qty: 0 }
  }
}

// ── Stock edit ───────────────────────────────────────────────────────────────
interface EditState { variantId: string; draftDelta: number }
const editing = ref<EditState | null>(null)

function startEdit(v: AdminVariant)  { editing.value = { variantId: v.id, draftDelta: 0 } }
function cancelEdit()                { editing.value = null }

async function saveStock(v: AdminVariant) {
  if (!editing.value || editing.value.variantId !== v.id) return
  saving.value = v.id
  await store.adjustStock(v.id, editing.value.draftDelta)
  saving.value = null
  editing.value = null
}

// ── Image upload ─────────────────────────────────────────────────────────────
async function onImageUpload(e: Event, productId: string, variantId: string) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  imageUploading.value = true
  try {
    const image = await uploadVariantImage(productId, variantId, file)
    for (const product of store.products) {
      const variant = product.variants.find(v => v.id === variantId)
      if (variant) { variant.images.push(image); break }
    }
  } catch (e: any) {
    store.error = e?.response?.data?.detail ?? 'Image upload failed'
  } finally {
    imageUploading.value = false }
}

// ── Filtering ────────────────────────────────────────────────────────────────
const filtered = computed(() =>
  store.products.filter(p => {
    if (!p.is_active) return false
    if (lineFilter.value !== 'all' && p.line !== lineFilter.value) return false
    if (stockFilter.value === 'low'  && !p.variants.some(v => v.is_active && v.stock_qty <= 15)) return false
    if (stockFilter.value === 'crit' && !p.variants.some(v => v.is_active && v.stock_qty <= 5))  return false
    if (!search.value) return true
    const q = search.value.toLowerCase()
    return p.name.toLowerCase().includes(q) || LINE_LABELS[p.line].toLowerCase().includes(q) ||
      p.variants.some(v => v.sku.toLowerCase().includes(q))
  })
)

function variantStatus(qty: number): AdminStatus {
  if (qty <= 5) return 'critico'
  if (qty <= 15) return 'bajo'
  return 'ok'
}

function totalStock(p: AdminProduct) {
  return p.variants.filter(v => v.is_active).reduce((s, v) => s + v.stock_qty, 0)
}

const expanded = ref<Set<string>>(new Set())
function toggleExpand(id: string) {
  expanded.value.has(id) ? expanded.value.delete(id) : expanded.value.add(id)
}

// ── KPI computed ─────────────────────────────────────────────────────────────
const activeVariants = computed(() =>
  store.products.flatMap(p => p.variants.filter(v => v.is_active))
)
const totalSKUs   = computed(() => activeVariants.value.length)
const totalUnits  = computed(() => activeVariants.value.reduce((s, v) => s + v.stock_qty, 0))
const lowStockQty = computed(() => activeVariants.value.filter(v => v.stock_qty <= 15).length)
const valorInventario = computed(() => {
  const total = activeVariants.value.reduce((s, v) => s + Number(v.price_usd) * v.stock_qty, 0)
  return total >= 1000 ? `$${(total / 1000).toFixed(1)}k` : `$${total.toFixed(0)}`
})
const totalImages = computed(() => activeVariants.value.reduce((s, v) => s + v.images.length, 0))
const productCount = computed(() => store.products.filter(p => p.is_active).length)

const LINE_OPTIONS: { value: ProductLine; label: string }[] = [
  { value: 'polo_atelier', label: 'Polo Atelier' },
  { value: 'signature',    label: 'Signature' },
  { value: 'essential',    label: 'Essential' },
]
const STYLE_OPTIONS: { value: ProductStyle; label: string }[] = [
  { value: 'classic', label: 'Classic' },
  { value: 'design',  label: 'Design'  },
]
const SIZE_OPTIONS: ProductSize[] = ['S', 'M', 'L', 'XL', 'XXL', 'XXXL']

onMounted(() => store.loadProducts())
</script>

<template>
  <div class="space-y-5">

    <!-- Actions -->
    <div class="flex justify-end gap-2">
      <AdminButton variant="ghost" @click="showAddVariant = store.products[0]?.id ?? null">
        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        Variante
      </AdminButton>
      <AdminButton variant="primary" @click="showAddProduct = true">
        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        Nuevo Producto
      </AdminButton>
    </div>

    <!-- Error -->
    <div v-if="store.error" class="px-4 py-3 rounded-lg text-[0.82rem] flex items-center justify-between" style="background: var(--status-crit-bg); color: var(--status-crit-text);">
      {{ store.error }}
      <button @click="store.error = null">✕</button>
    </div>

    <!-- KPI cards -->
    <div class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-5 gap-3">
      <AdminStatCard
        label="Total SKUs"
        :value="String(totalSKUs)"
        :sub="`en ${productCount} productos`"
        icon="M20 7H4a2 2 0 00-2 2v6a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2zM16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16"
      />
      <AdminStatCard
        label="Stock Total"
        :value="totalUnits.toLocaleString()"
        sub="unidades"
        icon="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"
      />
      <AdminStatCard
        label="Stock Bajo"
        :value="String(lowStockQty)"
        sub="variantes ≤ 50 uds"
        :value-color="lowStockQty > 0 ? 'var(--status-warn-text)' : undefined"
        icon="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
      />
      <AdminStatCard
        label="Valor Inventario"
        :value="valorInventario"
        sub="a precio de costo"
        icon="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
      />
      <AdminStatCard
        label="Imágenes"
        :value="String(totalImages)"
        sub="Cloudflare R2"
        icon="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
      />
    </div>

    <!-- Products & Variants table -->
    <div class="bg-white rounded-xl overflow-hidden" style="box-shadow: var(--admin-card-shadow);">
      <!-- Table header -->
      <div class="px-6 py-4 flex items-center justify-between" style="border-bottom: 1px solid var(--admin-border);">
        <p class="text-[0.72rem] font-semibold uppercase tracking-wider" style="color: var(--admin-text-primary);">Productos &amp; Variantes</p>
      </div>

      <!-- Filters -->
      <div class="px-6 py-3 flex items-center gap-3 flex-wrap" style="border-bottom: 1px solid var(--admin-border);">
        <AdminFilterBar v-model="search" placeholder="Buscar producto o SKU…">
          <select
            v-model="lineFilter"
            class="h-8 px-3 text-[0.75rem] rounded-lg appearance-none cursor-pointer focus:outline-none"
            style="border: 1.5px solid rgba(0,0,0,0.1); color: var(--admin-text-primary); background: white;"
          >
            <option value="all">Todas las líneas</option>
            <option v-for="opt in LINE_OPTIONS" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
          </select>
          <select
            v-model="stockFilter"
            class="h-8 px-3 text-[0.75rem] rounded-lg appearance-none cursor-pointer focus:outline-none"
            style="border: 1.5px solid rgba(0,0,0,0.1); color: var(--admin-text-primary); background: white;"
          >
            <option value="all">Todo el stock</option>
            <option value="low">Stock bajo (≤ 15)</option>
            <option value="crit">Crítico (≤ 5)</option>
          </select>
        </AdminFilterBar>
      </div>

      <!-- Skeleton -->
      <div v-if="store.loading" class="space-y-1 p-4">
        <div v-for="i in 4" :key="i" class="h-12 rounded-lg animate-pulse" style="background: rgba(0,0,0,0.05);" />
      </div>

      <!-- Empty -->
      <div v-else-if="filtered.length === 0" class="py-16 text-center">
        <p class="text-[0.85rem]" style="color: var(--admin-text-secondary);">
          {{ search ? `No hay productos que coincidan con "${search}"` : 'Sin productos aún.' }}
        </p>
        <button v-if="!search" class="mt-3 text-[0.75rem] underline" style="color: var(--admin-amber);" @click="showAddProduct = true">
          Crear primer producto →
        </button>
      </div>

      <!-- Table -->
      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr style="background: var(--admin-bg);">
              <th class="px-5 py-3 text-left font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Producto / Variante</th>
              <th class="px-5 py-3 text-left font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">SKU</th>
              <th class="px-5 py-3 text-left font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Talla</th>
              <th class="px-5 py-3 text-left font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Color</th>
              <th class="px-5 py-3 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Precio</th>
              <th class="px-5 py-3 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Costo</th>
              <th class="px-5 py-3 text-left font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Stock</th>
              <th class="px-5 py-3 text-center font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Estado</th>
              <th class="px-5 py-3 text-center font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="product in filtered" :key="product.id">
              <!-- Product group row -->
              <tr
                class="cursor-pointer transition-colors duration-100"
                style="background: rgba(201,168,76,0.04); border-bottom: 1px solid rgba(0,0,0,0.04);"
                @click="toggleExpand(product.id)"
              >
                <td class="px-5 py-3" colspan="8">
                  <div class="flex items-center gap-2">
                    <svg
                      class="w-3.5 h-3.5 flex-shrink-0 transition-transform duration-200"
                      :class="expanded.has(product.id) ? 'rotate-90' : ''"
                      style="color: var(--admin-text-secondary);"
                      viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                    ><polyline points="9 18 15 12 9 6"/></svg>
                    <svg class="w-4 h-4 flex-shrink-0" style="color: var(--admin-amber);" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <path d="M20 7H4a2 2 0 00-2 2v6a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2zM16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <span class="text-[0.82rem] font-semibold" style="color: var(--admin-text-primary);">{{ product.name }}</span>
                    <span class="text-[0.7rem]" style="color: var(--admin-text-secondary);">
                      {{ product.variants.filter(v => v.is_active).length }} variantes · {{ LINE_LABELS[product.line] }}
                    </span>
                  </div>
                </td>
                <td class="px-5 py-3 text-center">
                  <button
                    class="w-7 h-7 rounded-lg flex items-center justify-center transition-colors duration-150"
                    style="background: rgba(0,0,0,0.05); color: var(--admin-text-secondary);"
                    @click.stop="showAddVariant = product.id"
                  >
                    <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
                    </svg>
                  </button>
                </td>
              </tr>

              <!-- Variant rows -->
              <template v-if="expanded.has(product.id)">
                <tr
                  v-for="variant in product.variants.filter(v => v.is_active)"
                  :key="variant.id"
                  class="transition-colors duration-100"
                  style="border-bottom: 1px solid rgba(0,0,0,0.03);"
                >
                  <!-- Name -->
                  <td class="px-5 py-2.5 pl-10 text-[0.78rem]" style="color: var(--admin-text-secondary);">
                    <span class="opacity-40 mr-1">↳</span>{{ product.name }}
                  </td>
                  <!-- SKU -->
                  <td class="px-5 py-2.5 font-mono text-[0.68rem]" style="color: var(--admin-text-secondary);">{{ variant.sku }}</td>
                  <!-- Talla -->
                  <td class="px-5 py-2.5 text-[0.78rem]" style="color: var(--admin-text-primary);">{{ variant.size }}</td>
                  <!-- Color -->
                  <td class="px-5 py-2.5 text-[0.78rem]" style="color: var(--admin-text-primary);">
                    <div class="flex items-center gap-1.5">
                      <span class="w-2.5 h-2.5 rounded-full flex-shrink-0 border border-black/10" :style="{ background: variant.color.toLowerCase() === 'negro' ? '#111' : variant.color.toLowerCase() === 'blanco' ? '#f5f5f0' : variant.color.toLowerCase() === 'beige' ? '#d4c5a9' : variant.color.toLowerCase() === 'ivory' ? '#f5f0e8' : '#aaa' }" />
                      {{ variant.color }}
                    </div>
                  </td>
                  <!-- Precio -->
                  <td class="px-5 py-2.5 text-right text-[0.78rem] font-medium" style="color: var(--admin-text-primary);">${{ Number(variant.price_usd).toFixed(0) }}</td>
                  <!-- Costo -->
                  <td class="px-5 py-2.5 text-right text-[0.75rem]" style="color: var(--admin-text-secondary);">${{ Number(variant.cost_acquisition_usd).toFixed(0) }}</td>
                  <!-- Stock -->
                  <td class="px-5 py-2.5 min-w-[120px]">
                    <template v-if="editing?.variantId === variant.id">
                      <div class="flex items-center gap-1.5">
                        <span class="text-[0.75rem]" style="color: var(--admin-text-secondary);">{{ variant.stock_qty }} +</span>
                        <input
                          v-model.number="editing.draftDelta"
                          type="number"
                          class="w-14 text-right text-[0.78rem] border rounded px-2 py-0.5 focus:outline-none"
                          style="border-color: var(--admin-amber); color: var(--admin-text-primary);"
                        />
                      </div>
                    </template>
                    <template v-else>
                      <StockBar :current="variant.stock_qty" :threshold="50" />
                    </template>
                  </td>
                  <!-- Estado -->
                  <td class="px-5 py-2.5 text-center">
                    <StatusBadge :status="variantStatus(variant.stock_qty)" />
                  </td>
                  <!-- Acciones -->
                  <td class="px-5 py-2.5 text-center">
                    <div class="flex items-center justify-center gap-1.5">
                      <template v-if="editing?.variantId === variant.id">
                        <button
                          class="text-[0.7rem] px-2 py-1 rounded transition-colors"
                          style="color: var(--admin-text-secondary);"
                          @click="cancelEdit"
                        >Cancelar</button>
                        <button
                          class="text-[0.7rem] px-2.5 py-1 rounded font-medium text-white transition-opacity disabled:opacity-50 flex items-center gap-1"
                          style="background: var(--admin-amber);"
                          :disabled="saving === variant.id"
                          @click="saveStock(variant)"
                        >
                          <span v-if="saving === variant.id" class="w-2.5 h-2.5 border border-current border-t-transparent rounded-full animate-spin" />
                          Guardar
                        </button>
                      </template>
                      <template v-else>
                        <button
                          class="w-7 h-7 rounded-lg flex items-center justify-center transition-colors duration-150"
                          style="background: rgba(0,0,0,0.05); color: var(--admin-text-secondary);"
                          title="Editar stock"
                          @click="startEdit(variant)"
                        >
                          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
                            <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
                          </svg>
                        </button>
                        <button
                          class="w-7 h-7 rounded-lg flex items-center justify-center transition-colors duration-150"
                          style="background: rgba(0,0,0,0.05); color: var(--admin-text-secondary);"
                          title="Imágenes"
                          @click="showImages = { productId: product.id, variant }"
                        >
                          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
                            <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
                          </svg>
                        </button>
                      </template>
                    </div>
                  </td>
                </tr>
              </template>
            </template>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- ── Add Product Modal ──────────────────────────────────────────────── -->
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="showAddProduct" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="showAddProduct = false" />
        <div class="relative w-full max-w-md bg-white rounded-2xl shadow-2xl p-6 space-y-5">
          <div class="flex items-center justify-between">
            <h2 class="text-[0.9rem] font-semibold" style="color: var(--admin-text-primary);">Nuevo Producto</h2>
            <button class="text-[0.9rem]" style="color: var(--admin-text-secondary);" @click="showAddProduct = false">✕</button>
          </div>
          <div class="space-y-4">
            <div>
              <label class="text-[0.65rem] uppercase tracking-wider block mb-1.5" style="color: var(--admin-text-secondary);">Línea de Producto</label>
              <select v-model="newProduct.line" class="w-full border rounded-lg px-3 py-2 text-[0.82rem] focus:outline-none" style="border-color: rgba(0,0,0,0.12); color: var(--admin-text-primary);">
                <option v-for="opt in LINE_OPTIONS" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
              </select>
            </div>
            <div>
              <label class="text-[0.65rem] uppercase tracking-wider block mb-1.5" style="color: var(--admin-text-secondary);">Nombre</label>
              <input v-model="newProduct.name" type="text" placeholder="ej. Varsovia" class="w-full border rounded-lg px-3 py-2 text-[0.82rem] focus:outline-none" style="border-color: rgba(0,0,0,0.12); color: var(--admin-text-primary);" />
            </div>
            <div>
              <label class="text-[0.65rem] uppercase tracking-wider block mb-1.5" style="color: var(--admin-text-secondary);">Descripción <span class="normal-case">(opcional)</span></label>
              <textarea v-model="newProduct.description" rows="3" class="w-full border rounded-lg px-3 py-2 text-[0.82rem] focus:outline-none resize-none" style="border-color: rgba(0,0,0,0.12); color: var(--admin-text-primary);" />
            </div>
          </div>
          <div class="flex justify-end gap-3 pt-1">
            <button class="text-[0.75rem] px-4 py-2" style="color: var(--admin-text-secondary);" @click="showAddProduct = false">Cancelar</button>
            <AdminButton variant="primary" :disabled="!newProduct.name.trim()" :loading="creatingProduct" @click="submitAddProduct">
              Crear Producto
            </AdminButton>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>

  <!-- ── Add Variant Modal ──────────────────────────────────────────────── -->
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="showAddVariant" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="showAddVariant = null" />
        <div class="relative w-full max-w-md bg-white rounded-2xl shadow-2xl p-6 space-y-5">
          <div class="flex items-center justify-between">
            <h2 class="text-[0.9rem] font-semibold" style="color: var(--admin-text-primary);">Agregar Variante</h2>
            <button style="color: var(--admin-text-secondary);" @click="showAddVariant = null">✕</button>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="text-[0.65rem] uppercase tracking-wider block mb-1.5" style="color: var(--admin-text-secondary);">Estilo</label>
              <select v-model="newVariant.style" class="w-full border rounded-lg px-3 py-2 text-[0.82rem] focus:outline-none" style="border-color: rgba(0,0,0,0.12);">
                <option v-for="s in STYLE_OPTIONS" :key="s.value" :value="s.value">{{ s.label }}</option>
              </select>
            </div>
            <div>
              <label class="text-[0.65rem] uppercase tracking-wider block mb-1.5" style="color: var(--admin-text-secondary);">Talla</label>
              <select v-model="newVariant.size" class="w-full border rounded-lg px-3 py-2 text-[0.82rem] focus:outline-none" style="border-color: rgba(0,0,0,0.12);">
                <option v-for="sz in SIZE_OPTIONS" :key="sz" :value="sz">{{ sz }}</option>
              </select>
            </div>
            <div class="col-span-2">
              <label class="text-[0.65rem] uppercase tracking-wider block mb-1.5" style="color: var(--admin-text-secondary);">Color</label>
              <input v-model="newVariant.color" type="text" placeholder="ej. Ivory, Negro" class="w-full border rounded-lg px-3 py-2 text-[0.82rem] focus:outline-none" style="border-color: rgba(0,0,0,0.12);" />
            </div>
            <div>
              <label class="text-[0.65rem] uppercase tracking-wider block mb-1.5" style="color: var(--admin-text-secondary);">Precio USD</label>
              <input v-model.number="newVariant.price_usd" type="number" min="0" step="0.01" class="w-full border rounded-lg px-3 py-2 text-[0.82rem] focus:outline-none" style="border-color: rgba(0,0,0,0.12);" />
            </div>
            <div>
              <label class="text-[0.65rem] uppercase tracking-wider block mb-1.5" style="color: var(--admin-text-secondary);">Costo USD</label>
              <input v-model.number="newVariant.cost_acquisition_usd" type="number" min="0" step="0.01" class="w-full border rounded-lg px-3 py-2 text-[0.82rem] focus:outline-none" style="border-color: rgba(0,0,0,0.12);" />
            </div>
            <div>
              <label class="text-[0.65rem] uppercase tracking-wider block mb-1.5" style="color: var(--admin-text-secondary);">Stock Inicial</label>
              <input v-model.number="newVariant.stock_qty" type="number" min="0" class="w-full border rounded-lg px-3 py-2 text-[0.82rem] focus:outline-none" style="border-color: rgba(0,0,0,0.12);" />
            </div>
          </div>
          <div class="flex justify-end gap-3 pt-1">
            <button class="text-[0.75rem] px-4 py-2" style="color: var(--admin-text-secondary);" @click="showAddVariant = null">Cancelar</button>
            <AdminButton variant="primary" :disabled="!newVariant.color.trim() || newVariant.price_usd <= 0" :loading="creatingVariant" @click="submitAddVariant(showAddVariant!)">
              Agregar Variante
            </AdminButton>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>

  <!-- ── Image Manager Modal ────────────────────────────────────────────── -->
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="showImages" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="showImages = null" />
        <div class="relative w-full max-w-lg bg-white rounded-2xl shadow-2xl p-6 space-y-5">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-[0.9rem] font-semibold" style="color: var(--admin-text-primary);">Imágenes</h2>
              <p class="text-[0.72rem] font-mono mt-0.5" style="color: var(--admin-text-secondary);">{{ showImages.variant.sku }}</p>
            </div>
            <button style="color: var(--admin-text-secondary);" @click="showImages = null">✕</button>
          </div>
          <div v-if="showImages.variant.images.length > 0" class="grid grid-cols-3 gap-3">
            <div
              v-for="img in showImages.variant.images"
              :key="img.id"
              class="relative aspect-square rounded-xl overflow-hidden border"
              style="border-color: var(--admin-border);"
            >
              <img :src="img.url" :alt="img.alt_text ?? ''" class="w-full h-full object-cover" />
            </div>
          </div>
          <p v-else class="text-[0.82rem] text-center py-4" style="color: var(--admin-text-secondary);">Sin imágenes aún</p>
          <label class="flex flex-col items-center justify-center gap-2 w-full border-2 border-dashed rounded-xl py-5 cursor-pointer transition-colors" style="border-color: rgba(0,0,0,0.12);">
            <svg v-if="!imageUploading" class="w-5 h-5" style="color: var(--admin-text-secondary);" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M17 8l-5-5-5 5M12 3v12" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span v-if="imageUploading" class="w-5 h-5 border-2 border-t-transparent rounded-full animate-spin" style="border-color: var(--admin-amber);" />
            <span class="text-[0.72rem] uppercase tracking-wider" style="color: var(--admin-text-secondary);">
              {{ imageUploading ? 'Subiendo…' : 'Subir imagen' }}
            </span>
            <input type="file" accept="image/jpeg,image/png,image/webp" class="sr-only" :disabled="imageUploading" @change="(e) => onImageUpload(e, showImages!.productId, showImages!.variant.id)" />
          </label>
          <p class="text-[0.68rem] text-center" style="color: var(--admin-text-secondary);">JPEG, PNG, WebP · máx 10 MB</p>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-enter-active { transition: opacity 0.15s ease, transform 0.15s ease; }
.modal-leave-active { transition: opacity 0.1s ease, transform 0.1s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
</style>
