<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAdminInventoryStore } from '../store'
import { LINE_LABELS, STYLE_LABELS } from '@features/products/types'
import type { AdminProduct, AdminVariant, ProductCreatePayload, VariantCreatePayload, ProductLine, ProductStyle, ProductSize } from '../types'
import { uploadVariantImage } from '../api'

const store = useAdminInventoryStore()

const search = ref('')
const saving = ref<string | null>(null)
const showAddProduct = ref(false)
const showAddVariant = ref<string | null>(null) // productId
const showImages = ref<{ productId: string; variant: AdminVariant } | null>(null)
const imageUploading = ref(false)

// ── Add Product form ─────────────────────────────────────────────────────────

const newProduct = ref<ProductCreatePayload>({
  line: 'polo_atelier',
  name: '',
  description: '',
})
const creatingProduct = ref(false)

async function submitAddProduct() {
  if (!newProduct.value.name.trim()) return
  creatingProduct.value = true
  const product = await store.createProduct({
    ...newProduct.value,
    description: newProduct.value.description || undefined,
  })
  creatingProduct.value = false
  if (product) {
    showAddProduct.value = false
    newProduct.value = { line: 'polo_atelier', name: '', description: '' }
  }
}

// ── Add Variant form ─────────────────────────────────────────────────────────

const newVariant = ref<VariantCreatePayload>({
  style: 'classic',
  size: 'M',
  color: '',
  price_usd: 0,
  cost_acquisition_usd: 0,
  stock_qty: 0,
})
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

// ── Stock adjustment ─────────────────────────────────────────────────────────

interface EditState { variantId: string; draftDelta: number }
const editing = ref<EditState | null>(null)

function startEdit(v: AdminVariant) {
  editing.value = { variantId: v.id, draftDelta: 0 }
}

function cancelEdit() {
  editing.value = null
}

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
    // Update variant images in store
    for (const product of store.products) {
      const variant = product.variants.find(v => v.id === variantId)
      if (variant) {
        variant.images.push(image)
        break
      }
    }
  } catch (e: any) {
    store.error = e?.response?.data?.detail ?? 'Image upload failed'
  } finally {
    imageUploading.value = false
  }
}

// ── Filtering ────────────────────────────────────────────────────────────────

const filtered = computed(() =>
  store.products.filter(p => {
    if (!p.is_active) return false
    if (!search.value) return true
    const q = search.value.toLowerCase()
    return (
      p.name.toLowerCase().includes(q) ||
      LINE_LABELS[p.line].toLowerCase().includes(q)
    )
  })
)

function totalStock(p: AdminProduct) {
  return p.variants.filter(v => v.is_active).reduce((s, v) => s + v.stock_qty, 0)
}

function hasLowStock(p: AdminProduct) {
  return p.variants.some(v => v.is_active && v.stock_qty <= 5)
}

const expanded = ref<Set<string>>(new Set())
function toggleExpand(id: string) {
  expanded.value.has(id) ? expanded.value.delete(id) : expanded.value.add(id)
}

const LINE_OPTIONS: { value: ProductLine; label: string }[] = [
  { value: 'polo_atelier', label: 'Polo Atelier' },
  { value: 'signature', label: 'Signature' },
  { value: 'essential', label: 'Essential' },
]

const STYLE_OPTIONS: { value: ProductStyle; label: string }[] = [
  { value: 'classic', label: 'Classic' },
  { value: 'design', label: 'Design' },
]

const SIZE_OPTIONS: ProductSize[] = ['S', 'M', 'L', 'XL', 'XXL', 'XXXL']

onMounted(() => store.loadProducts())
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-end justify-between gap-4">
      <div>
        <p class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)]">Catalog</p>
        <h1 class="mt-1 text-2xl font-semibold uppercase tracking-wider text-[color:var(--color-obsidian)]">Inventory</h1>
      </div>
      <button
        class="flex items-center gap-2 px-4 py-2.5 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-xs uppercase tracking-widest rounded-[var(--radius-md)] hover:opacity-80 transition-opacity"
        @click="showAddProduct = true"
      >
        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        Add Product
      </button>
    </div>

    <!-- Error banner -->
    <div v-if="store.error" class="px-4 py-3 bg-red-50 border border-red-200 rounded-[var(--radius-md)] text-sm text-red-700 flex items-center justify-between">
      {{ store.error }}
      <button class="text-red-400 hover:text-red-600" @click="store.error = null">✕</button>
    </div>

    <!-- Search -->
    <div class="relative max-w-sm">
      <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[color:var(--color-border-strong)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35" stroke-linecap="round"/>
      </svg>
      <input
        v-model="search"
        type="text"
        placeholder="Search products…"
        class="w-full pl-9 pr-4 py-2 text-sm border border-[color:var(--color-border)] rounded-[var(--radius-md)] bg-[color:var(--color-ivory)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors"
      />
    </div>

    <!-- Skeleton -->
    <div v-if="store.loading" class="space-y-3">
      <div v-for="i in 4" :key="i" class="h-16 rounded-[var(--radius-md)] bg-[color:var(--color-warm-beige-dk)] animate-pulse" />
    </div>

    <!-- Empty state -->
    <div v-else-if="filtered.length === 0 && !search" class="py-16 text-center">
      <p class="text-sm text-[color:var(--color-border-strong)]">No products yet.</p>
      <button class="mt-3 text-xs uppercase tracking-widest text-[color:var(--color-obsidian)] underline" @click="showAddProduct = true">
        Create your first product →
      </button>
    </div>

    <!-- Product rows -->
    <div v-else class="space-y-2">
      <div
        v-for="product in filtered"
        :key="product.id"
        class="bg-[color:var(--color-ivory)] border rounded-[var(--radius-md)] overflow-hidden"
        :class="hasLowStock(product) ? 'border-amber-300' : 'border-[color:var(--color-border)]'"
      >
        <!-- Product header row -->
        <button
          class="w-full flex items-center gap-4 px-5 py-4 hover:bg-[color:var(--color-warm-beige)] transition-colors text-left"
          @click="toggleExpand(product.id)"
        >
          <svg
            class="w-4 h-4 flex-shrink-0 text-[color:var(--color-border-strong)] transition-transform duration-200"
            :class="expanded.has(product.id) ? 'rotate-90' : ''"
            viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
          >
            <polyline points="9 18 15 12 9 6"/>
          </svg>

          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-[color:var(--color-obsidian)] truncate">{{ product.name }}</p>
            <p class="text-xs text-[color:var(--color-border-strong)] mt-0.5 uppercase tracking-wider">{{ LINE_LABELS[product.line] }}</p>
          </div>

          <div class="flex items-center gap-6 flex-shrink-0">
            <div class="text-right">
              <p class="text-xs text-[color:var(--color-border-strong)]">{{ product.variants.filter(v => v.is_active).length }} variants</p>
              <p class="text-sm font-medium text-[color:var(--color-obsidian)]">{{ totalStock(product) }} units</p>
            </div>
            <span
              v-if="hasLowStock(product)"
              class="text-xs px-2 py-0.5 rounded-full bg-amber-50 text-amber-700 font-medium"
            >Low Stock</span>
          </div>
        </button>

        <!-- Variants table -->
        <Transition name="variants-expand">
          <div v-if="expanded.has(product.id)" class="border-t border-[color:var(--color-border)]">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-[color:var(--color-warm-beige)] text-xs uppercase tracking-widest text-[color:var(--color-border-strong)]">
                  <th class="px-5 py-2.5 text-left font-medium">SKU</th>
                  <th class="px-5 py-2.5 text-left font-medium">Style</th>
                  <th class="px-5 py-2.5 text-left font-medium">Color</th>
                  <th class="px-5 py-2.5 text-left font-medium">Size</th>
                  <th class="px-5 py-2.5 text-right font-medium">Price</th>
                  <th class="px-5 py-2.5 text-right font-medium">Stock</th>
                  <th class="px-5 py-2.5 text-right font-medium">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-[color:var(--color-border)]">
                <tr
                  v-for="variant in product.variants.filter(v => v.is_active)"
                  :key="variant.id"
                  :class="variant.stock_qty <= 5 ? 'bg-amber-50/40' : ''"
                >
                  <td class="px-5 py-3 font-mono text-xs text-[color:var(--color-border-strong)]">{{ variant.sku }}</td>
                  <td class="px-5 py-3 text-[color:var(--color-obsidian)]">{{ STYLE_LABELS[variant.style] }}</td>
                  <td class="px-5 py-3 text-[color:var(--color-obsidian)]">{{ variant.color }}</td>
                  <td class="px-5 py-3 text-[color:var(--color-obsidian)]">{{ variant.size }}</td>
                  <td class="px-5 py-3 text-right text-[color:var(--color-obsidian)]">${{ Number(variant.price_usd).toFixed(2) }}</td>

                  <!-- Stock cell -->
                  <td class="px-5 py-3 text-right">
                    <template v-if="editing?.variantId === variant.id">
                      <div class="flex items-center justify-end gap-1.5">
                        <span class="text-xs text-[color:var(--color-border-strong)]">{{ variant.stock_qty }}</span>
                        <span class="text-xs text-[color:var(--color-border-strong)]">+</span>
                        <input
                          v-model.number="editing.draftDelta"
                          type="number"
                          class="w-16 text-right border border-[color:var(--color-obsidian)] rounded-[var(--radius-sm)] px-2 py-0.5 text-sm focus:outline-none"
                        />
                      </div>
                    </template>
                    <template v-else>
                      <span
                        class="font-medium"
                        :class="variant.stock_qty === 0 ? 'text-red-600' : variant.stock_qty <= 5 ? 'text-amber-600' : 'text-[color:var(--color-obsidian)]'"
                      >{{ variant.stock_qty }}</span>
                      <span v-if="variant.stock_qty === 0" class="ml-1 text-xs text-red-500">Out</span>
                    </template>
                  </td>

                  <!-- Actions cell -->
                  <td class="px-5 py-3 text-right">
                    <div class="flex items-center justify-end gap-3">
                      <template v-if="editing?.variantId === variant.id">
                        <button
                          class="text-xs text-[color:var(--color-border-strong)] hover:text-[color:var(--color-obsidian)] uppercase tracking-wider"
                          @click="cancelEdit"
                        >Cancel</button>
                        <button
                          class="text-xs bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] px-2.5 py-1 rounded-[var(--radius-sm)] hover:opacity-80 flex items-center gap-1.5"
                          :disabled="saving === variant.id"
                          @click="saveStock(variant)"
                        >
                          <span v-if="saving === variant.id" class="w-2.5 h-2.5 border border-current border-t-transparent rounded-full animate-spin" />
                          Save
                        </button>
                      </template>
                      <template v-else>
                        <button
                          class="text-xs text-[color:var(--color-border-strong)] hover:text-[color:var(--color-obsidian)] uppercase tracking-wider"
                          @click="showImages = { productId: product.id, variant }"
                        >Images</button>
                        <button
                          class="text-xs text-[color:var(--color-border-strong)] hover:text-[color:var(--color-obsidian)] uppercase tracking-wider"
                          @click="startEdit(variant)"
                        >Stock</button>
                      </template>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>

            <!-- Add variant button -->
            <div class="px-5 py-3 border-t border-[color:var(--color-border)]">
              <button
                class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] hover:text-[color:var(--color-obsidian)] transition-colors flex items-center gap-1.5"
                @click="showAddVariant = product.id"
              >
                <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
                </svg>
                Add Variant
              </button>
            </div>
          </div>
        </Transition>
      </div>

      <p v-if="filtered.length === 0 && search" class="text-sm text-[color:var(--color-border-strong)] py-8 text-center">
        No products match "{{ search }}"
      </p>
    </div>
  </div>

  <!-- ── Add Product Modal ──────────────────────────────────────────────────── -->
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="showAddProduct" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="showAddProduct = false" />
        <div class="relative w-full max-w-md bg-[color:var(--color-ivory)] rounded-[var(--radius-lg)] shadow-2xl p-6 space-y-5">
          <div class="flex items-center justify-between">
            <h2 class="text-sm font-semibold uppercase tracking-wider text-[color:var(--color-obsidian)]">New Product</h2>
            <button class="text-[color:var(--color-border-strong)] hover:text-[color:var(--color-obsidian)]" @click="showAddProduct = false">✕</button>
          </div>

          <div class="space-y-4">
            <div>
              <label class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] mb-1.5 block">Product Line</label>
              <select
                v-model="newProduct.line"
                class="w-full border border-[color:var(--color-border)] rounded-[var(--radius-md)] px-3 py-2 text-sm bg-[color:var(--color-ivory)] focus:outline-none focus:border-[color:var(--color-obsidian)]"
              >
                <option v-for="opt in LINE_OPTIONS" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
              </select>
            </div>

            <div>
              <label class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] mb-1.5 block">Product Name</label>
              <input
                v-model="newProduct.name"
                type="text"
                placeholder="e.g. Polo Atelier Classic"
                class="w-full border border-[color:var(--color-border)] rounded-[var(--radius-md)] px-3 py-2 text-sm bg-[color:var(--color-ivory)] focus:outline-none focus:border-[color:var(--color-obsidian)]"
              />
            </div>

            <div>
              <label class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] mb-1.5 block">Description <span class="normal-case">(optional)</span></label>
              <textarea
                v-model="newProduct.description"
                rows="3"
                placeholder="Brief product description…"
                class="w-full border border-[color:var(--color-border)] rounded-[var(--radius-md)] px-3 py-2 text-sm bg-[color:var(--color-ivory)] focus:outline-none focus:border-[color:var(--color-obsidian)] resize-none"
              />
            </div>
          </div>

          <div class="flex justify-end gap-3 pt-1">
            <button
              class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] hover:text-[color:var(--color-obsidian)] px-4 py-2"
              @click="showAddProduct = false"
            >Cancel</button>
            <button
              class="flex items-center gap-2 px-5 py-2.5 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-xs uppercase tracking-widest rounded-[var(--radius-md)] hover:opacity-80 disabled:opacity-50"
              :disabled="!newProduct.name.trim() || creatingProduct"
              @click="submitAddProduct"
            >
              <span v-if="creatingProduct" class="w-3 h-3 border border-current border-t-transparent rounded-full animate-spin" />
              Create Product
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>

  <!-- ── Add Variant Modal ──────────────────────────────────────────────────── -->
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="showAddVariant" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="showAddVariant = null" />
        <div class="relative w-full max-w-md bg-[color:var(--color-ivory)] rounded-[var(--radius-lg)] shadow-2xl p-6 space-y-5">
          <div class="flex items-center justify-between">
            <h2 class="text-sm font-semibold uppercase tracking-wider text-[color:var(--color-obsidian)]">Add Variant</h2>
            <button class="text-[color:var(--color-border-strong)] hover:text-[color:var(--color-obsidian)]" @click="showAddVariant = null">✕</button>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] mb-1.5 block">Style</label>
              <select
                v-model="newVariant.style"
                class="w-full border border-[color:var(--color-border)] rounded-[var(--radius-md)] px-3 py-2 text-sm bg-[color:var(--color-ivory)] focus:outline-none focus:border-[color:var(--color-obsidian)]"
              >
                <option v-for="s in STYLE_OPTIONS" :key="s.value" :value="s.value">{{ s.label }}</option>
              </select>
            </div>
            <div>
              <label class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] mb-1.5 block">Size</label>
              <select
                v-model="newVariant.size"
                class="w-full border border-[color:var(--color-border)] rounded-[var(--radius-md)] px-3 py-2 text-sm bg-[color:var(--color-ivory)] focus:outline-none focus:border-[color:var(--color-obsidian)]"
              >
                <option v-for="sz in SIZE_OPTIONS" :key="sz" :value="sz">{{ sz }}</option>
              </select>
            </div>
            <div class="col-span-2">
              <label class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] mb-1.5 block">Color</label>
              <input
                v-model="newVariant.color"
                type="text"
                placeholder="e.g. Ivory, Obsidian"
                class="w-full border border-[color:var(--color-border)] rounded-[var(--radius-md)] px-3 py-2 text-sm bg-[color:var(--color-ivory)] focus:outline-none focus:border-[color:var(--color-obsidian)]"
              />
            </div>
            <div>
              <label class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] mb-1.5 block">Price USD</label>
              <input
                v-model.number="newVariant.price_usd"
                type="number"
                min="0"
                step="0.01"
                class="w-full border border-[color:var(--color-border)] rounded-[var(--radius-md)] px-3 py-2 text-sm bg-[color:var(--color-ivory)] focus:outline-none focus:border-[color:var(--color-obsidian)]"
              />
            </div>
            <div>
              <label class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] mb-1.5 block">Cost USD</label>
              <input
                v-model.number="newVariant.cost_acquisition_usd"
                type="number"
                min="0"
                step="0.01"
                class="w-full border border-[color:var(--color-border)] rounded-[var(--radius-md)] px-3 py-2 text-sm bg-[color:var(--color-ivory)] focus:outline-none focus:border-[color:var(--color-obsidian)]"
              />
            </div>
            <div>
              <label class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] mb-1.5 block">Initial Stock</label>
              <input
                v-model.number="newVariant.stock_qty"
                type="number"
                min="0"
                class="w-full border border-[color:var(--color-border)] rounded-[var(--radius-md)] px-3 py-2 text-sm bg-[color:var(--color-ivory)] focus:outline-none focus:border-[color:var(--color-obsidian)]"
              />
            </div>
          </div>

          <div class="flex justify-end gap-3 pt-1">
            <button
              class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)] hover:text-[color:var(--color-obsidian)] px-4 py-2"
              @click="showAddVariant = null"
            >Cancel</button>
            <button
              class="flex items-center gap-2 px-5 py-2.5 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-xs uppercase tracking-widest rounded-[var(--radius-md)] hover:opacity-80 disabled:opacity-50"
              :disabled="!newVariant.color.trim() || newVariant.price_usd <= 0 || creatingVariant"
              @click="submitAddVariant(showAddVariant!)"
            >
              <span v-if="creatingVariant" class="w-3 h-3 border border-current border-t-transparent rounded-full animate-spin" />
              Add Variant
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>

  <!-- ── Image Manager Modal ────────────────────────────────────────────────── -->
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="showImages" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="showImages = null" />
        <div class="relative w-full max-w-lg bg-[color:var(--color-ivory)] rounded-[var(--radius-lg)] shadow-2xl p-6 space-y-5">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-sm font-semibold uppercase tracking-wider text-[color:var(--color-obsidian)]">Images</h2>
              <p class="text-xs text-[color:var(--color-border-strong)] mt-0.5">{{ showImages.variant.sku }}</p>
            </div>
            <button class="text-[color:var(--color-border-strong)] hover:text-[color:var(--color-obsidian)]" @click="showImages = null">✕</button>
          </div>

          <!-- Existing images -->
          <div v-if="showImages.variant.images.length > 0" class="grid grid-cols-3 gap-3">
            <div
              v-for="img in showImages.variant.images"
              :key="img.id"
              class="relative aspect-square rounded-[var(--radius-md)] overflow-hidden border border-[color:var(--color-border)] group"
            >
              <img :src="img.url" :alt="img.alt_text ?? ''" class="w-full h-full object-cover" />
            </div>
          </div>
          <p v-else class="text-sm text-[color:var(--color-border-strong)] text-center py-4">No images yet</p>

          <!-- Upload -->
          <div>
            <label
              class="flex items-center justify-center gap-2 w-full border-2 border-dashed border-[color:var(--color-border)] rounded-[var(--radius-md)] py-4 cursor-pointer hover:border-[color:var(--color-obsidian)] transition-colors"
            >
              <svg v-if="!imageUploading" class="w-4 h-4 text-[color:var(--color-border-strong)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M17 8l-5-5-5 5M12 3v12" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span v-if="imageUploading" class="w-4 h-4 border border-[color:var(--color-obsidian)] border-t-transparent rounded-full animate-spin" />
              <span class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)]">
                {{ imageUploading ? 'Uploading…' : 'Upload Image' }}
              </span>
              <input
                type="file"
                accept="image/jpeg,image/png,image/webp"
                class="sr-only"
                :disabled="imageUploading"
                @change="(e) => onImageUpload(e, showImages!.productId, showImages!.variant.id)"
              />
            </label>
            <p class="mt-1.5 text-xs text-[color:var(--color-border-strong)] text-center">JPEG, PNG, WebP · max 10 MB</p>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.variants-expand-enter-active { transition: max-height 0.25s ease, opacity 0.2s ease; overflow: hidden; }
.variants-expand-leave-active { transition: max-height 0.15s ease, opacity 0.15s ease; overflow: hidden; }
.variants-expand-enter-from, .variants-expand-leave-to { max-height: 0; opacity: 0; }
.variants-expand-enter-to, .variants-expand-leave-from { max-height: 800px; opacity: 1; }

.modal-enter-active { transition: opacity 0.15s ease; }
.modal-leave-active { transition: opacity 0.1s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
</style>
