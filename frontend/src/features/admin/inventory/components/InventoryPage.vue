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

const SIZE_ORDER: ProductSize[] = ['S', 'M', 'L', 'XL', 'XXL', 'XXXL']

function productColors(p: AdminProduct): string[] {
  const seen = new Set<string>()
  const out: string[] = []
  for (const v of p.variants) {
    if (v.is_active && !seen.has(v.color)) { seen.add(v.color); out.push(v.color) }
  }
  return out
}

function findVariant(p: AdminProduct, size: ProductSize, color: string): AdminVariant | undefined {
  return p.variants.find(v => v.is_active && v.size === size && v.color === color)
}

function swatchHex(color: string): string {
  const map: Record<string, string> = {
    // Spanish
    negro: '#111111', blanco: '#f5f5f0', beige: '#d4c5a9',
    ivory: '#f5f0e8', crema: '#f0e8d8', gris: '#9ca3af', azul: '#2563eb',
    vino: '#7c2d3e', verde: '#16a34a', camel: '#c19a6b', rojo: '#dc2626',
    naranja: '#ea580c', amarillo: '#ca8a04', morado: '#7c3aed', rosa: '#db2777',
    cafe: '#92400e', marino: '#1e3a5f', menta: '#6ee7b7', lavanda: '#a78bfa',
    // English
    black: '#111111', white: '#f5f5f0', gray: '#9ca3af', grey: '#9ca3af',
    blue: '#2563eb', red: '#dc2626', orange: '#ea580c', yellow: '#ca8a04',
    green: '#16a34a', purple: '#7c3aed', pink: '#db2777', brown: '#92400e',
    navy: '#1e3a5f', mint: '#6ee7b7', lavender: '#a78bfa', cream: '#f0e8d8',
    tan: '#d4c5a9', khaki: '#c3b091', coral: '#ff6b6b', teal: '#0d9488',
    burgundy: '#7c2d3e', olive: '#6b7a2a', sand: '#d4c5a9', charcoal: '#374151',
  }
  return map[color.toLowerCase()] ?? '#888888'
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

      <!-- Product Cards (matrix layout) -->
      <div v-else class="p-4 space-y-4">
        <div
          v-for="product in filtered"
          :key="product.id"
          class="bg-white rounded-xl overflow-hidden"
          style="border: 1px solid var(--admin-border); box-shadow: var(--admin-card-shadow);"
        >
          <!-- Product header -->
          <div
            class="flex items-center justify-between px-5 py-3.5"
            style="border-bottom: 1px solid var(--admin-border); background: rgba(201,168,76,0.04);"
          >
            <div class="flex items-center gap-3 min-w-0">
              <svg class="w-4 h-4 flex-shrink-0" style="color: var(--admin-amber);" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M20 7H4a2 2 0 00-2 2v6a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2zM16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span class="text-[0.88rem] font-semibold" style="color: var(--admin-text-primary);">{{ product.name }}</span>
              <span
                class="text-[0.62rem] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full flex-shrink-0"
                style="background: rgba(201,168,76,0.12); color: var(--admin-amber);"
              >{{ LINE_LABELS[product.line] }}</span>
              <span class="text-[0.72rem] hidden sm:inline" style="color: var(--admin-text-secondary);">
                {{ totalStock(product) }} uds · {{ product.variants.filter(v => v.is_active).length }} variantes
              </span>
            </div>
            <button
              class="flex items-center gap-1.5 text-[0.72rem] font-medium px-3 py-1.5 rounded-lg transition-colors flex-shrink-0"
              style="background: rgba(0,0,0,0.05); color: var(--admin-text-secondary);"
              @click="showAddVariant = product.id"
            >
              <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
              Variante
            </button>
          </div>

          <!-- Size × Color matrix -->
          <div class="overflow-x-auto p-4">
            <table class="border-collapse">
              <thead>
                <tr>
                  <th class="pr-5 pb-3 text-left text-[0.6rem] font-semibold uppercase tracking-wider" style="color: var(--admin-text-secondary); min-width: 48px;">Talla</th>
                  <th
                    v-for="color in productColors(product)"
                    :key="color"
                    class="px-2 pb-3 text-center text-[0.6rem] font-semibold uppercase tracking-wider"
                    style="color: var(--admin-text-secondary); min-width: 96px;"
                  >
                    <div class="flex flex-col items-center gap-1.5">
                      <span
                        class="w-5 h-5 rounded-full border flex-shrink-0"
                        :style="{ background: swatchHex(color), borderColor: 'rgba(0,0,0,0.12)' }"
                      />
                      {{ color }}
                      <!-- Image manager trigger — always visible per color column -->
                      <button
                        v-if="product.variants.find(v => v.is_active && v.color === color)"
                        class="flex items-center gap-1 text-[0.6rem] font-semibold px-2 py-1 rounded-lg border transition-colors hover:opacity-80"
                        style="color: var(--admin-amber); background: rgba(201,168,76,0.08); border-color: rgba(201,168,76,0.3);"
                        title="Gestionar imágenes"
                        @click.stop="showImages = { productId: product.id, variant: product.variants.find(v => v.is_active && v.color === color)! }"
                      >
                        <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                          <circle cx="8.5" cy="8.5" r="1.5"/>
                          <polyline points="21 15 16 10 5 21"/>
                        </svg>
                        {{ product.variants.filter(v => v.is_active && v.color === color).reduce((n, v) => n + v.images.length, 0) }}
                      </button>
                    </div>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="size in SIZE_ORDER.filter(s => product.variants.some(v => v.is_active && v.size === s))"
                  :key="size"
                  style="border-top: 1px solid var(--admin-border);"
                >
                  <td class="pr-5 py-2 font-bold text-[0.82rem]" style="color: var(--admin-text-primary);">{{ size }}</td>
                  <td
                    v-for="color in productColors(product)"
                    :key="color"
                    class="px-2 py-2 text-center"
                  >
                    <template v-if="findVariant(product, size, color)">
                      <template v-if="editing?.variantId === findVariant(product, size, color)!.id">
                        <!-- Inline stock edit -->
                        <div class="flex flex-col items-center gap-1 py-1">
                          <span class="text-[0.65rem]" style="color: var(--admin-text-secondary);">
                            {{ findVariant(product, size, color)!.stock_qty }} +
                          </span>
                          <input
                            v-model.number="editing.draftDelta"
                            type="number"
                            class="w-14 text-center text-[0.75rem] border rounded px-1 py-0.5 focus:outline-none"
                            style="border-color: var(--admin-amber);"
                          />
                          <div class="flex gap-1">
                            <button
                              class="text-[0.62rem] px-1.5 py-0.5 rounded transition-colors"
                              style="color: var(--admin-text-secondary);"
                              @click="cancelEdit"
                            >✕</button>
                            <button
                              class="text-[0.62rem] px-1.5 py-0.5 rounded text-white font-medium disabled:opacity-50 flex items-center gap-0.5"
                              style="background: var(--admin-amber);"
                              :disabled="saving === findVariant(product, size, color)!.id"
                              @click="saveStock(findVariant(product, size, color)!)"
                            >
                              <span v-if="saving === findVariant(product, size, color)!.id" class="w-2 h-2 border border-current border-t-transparent rounded-full animate-spin inline-block" />
                              <span v-else>✓</span>
                            </button>
                          </div>
                        </div>
                      </template>
                      <template v-else>
                        <!-- Stock edit button + image trigger (sibling divs, no nested buttons) -->
                        <div class="group flex flex-col items-center gap-0.5">
                          <button
                            class="w-full flex flex-col items-center gap-0.5 rounded-lg px-2 py-2 transition-colors duration-100"
                            :class="variantStatus(findVariant(product, size, color)!.stock_qty) === 'critico' ? 'hover:bg-red-50'
                                   : variantStatus(findVariant(product, size, color)!.stock_qty) === 'bajo' ? 'hover:bg-amber-50'
                                   : 'hover:bg-green-50'"
                            :title="`Editar stock — SKU: ${findVariant(product, size, color)!.sku}`"
                            @click="startEdit(findVariant(product, size, color)!)"
                          >
                            <span
                              class="text-[0.95rem] font-bold tabular-nums leading-none"
                              :style="variantStatus(findVariant(product, size, color)!.stock_qty) === 'critico'
                                ? { color: 'var(--status-crit-text)' }
                                : variantStatus(findVariant(product, size, color)!.stock_qty) === 'bajo'
                                  ? { color: 'var(--status-warn-text)' }
                                  : { color: 'var(--status-ok-text)' }"
                            >{{ findVariant(product, size, color)!.stock_qty }}</span>
                            <span class="text-[0.62rem] tabular-nums" style="color: var(--admin-text-secondary);">
                              ${{ Number(findVariant(product, size, color)!.price_usd).toFixed(0) }}
                            </span>
                            <span class="text-[0.55rem] uppercase tracking-wider opacity-0 group-hover:opacity-60 transition-opacity" style="color: var(--admin-text-secondary);">editar</span>
                          </button>
                          <!-- Image trigger — sibling, never nested inside button -->
                          <button
                            class="text-[0.58rem] flex items-center gap-0.5 transition-opacity rounded px-1"
                            :class="findVariant(product, size, color)!.images.length > 0 ? 'opacity-80 hover:opacity-100' : 'opacity-50 hover:opacity-80'"
                            style="color: var(--admin-amber);"
                            title="Gestionar imágenes"
                            @click.stop="showImages = { productId: product.id, variant: findVariant(product, size, color)! }"
                          >
                            <svg class="w-2.5 h-2.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                              <circle cx="8.5" cy="8.5" r="1.5"/>
                              <polyline points="21 15 16 10 5 21"/>
                            </svg>
                            {{ findVariant(product, size, color)!.images.length }}
                          </button>
                        </div>
                      </template>
                    </template>
                    <template v-else>
                      <span class="text-[0.75rem]" style="color: rgba(0,0,0,0.15);">—</span>
                    </template>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
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
