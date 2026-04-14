<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

interface Variant {
  id: string
  sku: string
  size: string
  color: string
  stock: number
  editing: boolean
  draftStock: number
}

interface Product {
  id: string
  name: string
  line: string
  priceUSD: number
  variants: Variant[]
  expanded: boolean
}

const products = ref<Product[]>([])
const loading = ref(true)
const search = ref('')
const saving = ref<string | null>(null)

const LOW_STOCK = 5

const filtered = computed(() =>
  products.value.filter(p =>
    search.value === '' ||
    p.name.toLowerCase().includes(search.value.toLowerCase()) ||
    p.line.toLowerCase().includes(search.value.toLowerCase())
  )
)

function toggleExpand(p: Product) {
  p.expanded = !p.expanded
}

function startEdit(v: Variant) {
  v.draftStock = v.stock
  v.editing = true
}

function cancelEdit(v: Variant) {
  v.editing = false
}

async function saveStock(v: Variant) {
  saving.value = v.id
  await new Promise(r => setTimeout(r, 400))
  v.stock = v.draftStock
  v.editing = false
  saving.value = null
}

function totalStock(p: Product) {
  return p.variants.reduce((s, v) => s + v.stock, 0)
}

function hasLowStock(p: Product) {
  return p.variants.some(v => v.stock <= LOW_STOCK)
}

onMounted(() => {
  setTimeout(() => {
    products.value = [
      {
        id: 'p1', name: 'Polo Atelier — Classic', line: 'Polo Atelier', priceUSD: 180, expanded: false,
        variants: [
          { id: 'v1',  sku: 'PA-CL-IVY-S',  size: 'S', color: 'Ivory',    stock: 12, editing: false, draftStock: 0 },
          { id: 'v2',  sku: 'PA-CL-IVY-M',  size: 'M', color: 'Ivory',    stock: 8,  editing: false, draftStock: 0 },
          { id: 'v3',  sku: 'PA-CL-IVY-L',  size: 'L', color: 'Ivory',    stock: 3,  editing: false, draftStock: 0 },
          { id: 'v4',  sku: 'PA-CL-OBS-S',  size: 'S', color: 'Obsidian', stock: 10, editing: false, draftStock: 0 },
          { id: 'v5',  sku: 'PA-CL-OBS-M',  size: 'M', color: 'Obsidian', stock: 6,  editing: false, draftStock: 0 },
          { id: 'v6',  sku: 'PA-CL-OBS-L',  size: 'L', color: 'Obsidian', stock: 0,  editing: false, draftStock: 0 },
        ],
      },
      {
        id: 'p2', name: 'Polo Atelier — Design', line: 'Polo Atelier', priceUSD: 195, expanded: false,
        variants: [
          { id: 'v7',  sku: 'PA-DS-OBS-M',  size: 'M', color: 'Obsidian', stock: 9, editing: false, draftStock: 0 },
          { id: 'v8',  sku: 'PA-DS-OBS-L',  size: 'L', color: 'Obsidian', stock: 3, editing: false, draftStock: 0 },
          { id: 'v9',  sku: 'PA-DS-OBS-XL', size: 'XL', color: 'Obsidian', stock: 1, editing: false, draftStock: 0 },
        ],
      },
      {
        id: 'p3', name: 'Signature Shirt', line: 'Signature', priceUSD: 220, expanded: false,
        variants: [
          { id: 'v10', sku: 'SIG-DS-MID-M',  size: 'M', color: 'Midnight', stock: 7,  editing: false, draftStock: 0 },
          { id: 'v11', sku: 'SIG-DS-MID-L',  size: 'L', color: 'Midnight', stock: 4,  editing: false, draftStock: 0 },
          { id: 'v12', sku: 'SIG-DS-MID-XL', size: 'XL', color: 'Midnight', stock: 2, editing: false, draftStock: 0 },
        ],
      },
      {
        id: 'p4', name: 'Essential Tee', line: 'Essential', priceUSD: 95, expanded: false,
        variants: [
          { id: 'v13', sku: 'ESS-CL-IVY-S',  size: 'S', color: 'Ivory',      stock: 20, editing: false, draftStock: 0 },
          { id: 'v14', sku: 'ESS-CL-IVY-M',  size: 'M', color: 'Ivory',      stock: 15, editing: false, draftStock: 0 },
          { id: 'v15', sku: 'ESS-CL-WB-S',   size: 'S', color: 'Warm Beige', stock: 8,  editing: false, draftStock: 0 },
          { id: 'v16', sku: 'ESS-CL-WB-M',   size: 'M', color: 'Warm Beige', stock: 4,  editing: false, draftStock: 0 },
        ],
      },
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
        <p class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)]">Catalog</p>
        <h1 class="mt-1 text-2xl font-semibold uppercase tracking-wider text-[color:var(--color-obsidian)]">Inventory</h1>
      </div>
      <button class="flex items-center gap-2 px-4 py-2.5 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-xs uppercase tracking-widest rounded-[var(--radius-md)] hover:opacity-80 transition-opacity duration-[var(--duration-fast)]">
        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        Add Product
      </button>
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
    <div v-if="loading" class="space-y-3">
      <div v-for="i in 4" :key="i" class="h-16 rounded-[var(--radius-md)] bg-[color:var(--color-warm-beige-dk)] animate-pulse" />
    </div>

    <!-- Product rows -->
    <div v-else class="space-y-2">
      <div
        v-for="product in filtered"
        :key="product.id"
        class="bg-[color:var(--color-ivory)] border rounded-[var(--radius-md)] overflow-hidden transition-colors"
        :class="hasLowStock(product) ? 'border-amber-300' : 'border-[color:var(--color-border)]'"
      >
        <!-- Product row -->
        <button
          class="w-full flex items-center gap-4 px-5 py-4 hover:bg-[color:var(--color-warm-beige)] transition-colors duration-[var(--duration-fast)] text-left"
          @click="toggleExpand(product)"
        >
          <!-- Expand chevron -->
          <svg
            class="w-4 h-4 flex-shrink-0 text-[color:var(--color-border-strong)] transition-transform duration-[var(--duration-normal)]"
            :class="product.expanded ? 'rotate-90' : ''"
            viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
          >
            <polyline points="9 18 15 12 9 6"/>
          </svg>

          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-[color:var(--color-obsidian)] truncate">{{ product.name }}</p>
            <p class="text-xs text-[color:var(--color-border-strong)] mt-0.5 uppercase tracking-wider">{{ product.line }}</p>
          </div>

          <div class="flex items-center gap-6 flex-shrink-0">
            <div class="text-right">
              <p class="text-xs text-[color:var(--color-border-strong)]">{{ product.variants.length }} variants</p>
              <p class="text-sm font-medium text-[color:var(--color-obsidian)]">{{ totalStock(product) }} units</p>
            </div>
            <p class="text-sm font-medium text-[color:var(--color-obsidian)]">${{ product.priceUSD }}</p>
            <span
              v-if="hasLowStock(product)"
              class="text-xs px-2 py-0.5 rounded-full bg-amber-50 text-amber-700 font-medium"
            >Low Stock</span>
          </div>
        </button>

        <!-- Variants table -->
        <Transition name="variants-expand">
          <div v-if="product.expanded" class="border-t border-[color:var(--color-border)]">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-[color:var(--color-warm-beige)] text-xs uppercase tracking-widest text-[color:var(--color-border-strong)]">
                  <th class="px-5 py-2.5 text-left font-medium">SKU</th>
                  <th class="px-5 py-2.5 text-left font-medium">Color</th>
                  <th class="px-5 py-2.5 text-left font-medium">Size</th>
                  <th class="px-5 py-2.5 text-right font-medium">Stock</th>
                  <th class="px-5 py-2.5 text-right font-medium">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-[color:var(--color-border)]">
                <tr
                  v-for="variant in product.variants"
                  :key="variant.id"
                  class="transition-colors duration-[var(--duration-fast)]"
                  :class="variant.stock <= LOW_STOCK ? 'bg-amber-50/40' : ''"
                >
                  <td class="px-5 py-3 font-mono text-xs text-[color:var(--color-border-strong)]">{{ variant.sku }}</td>
                  <td class="px-5 py-3 text-[color:var(--color-obsidian)]">{{ variant.color }}</td>
                  <td class="px-5 py-3 text-[color:var(--color-obsidian)]">{{ variant.size }}</td>
                  <td class="px-5 py-3 text-right">
                    <!-- Inline edit -->
                    <span v-if="!variant.editing" class="flex items-center justify-end gap-2">
                      <span
                        class="font-medium text-sm"
                        :class="variant.stock === 0 ? 'text-red-600' : variant.stock <= LOW_STOCK ? 'text-amber-600' : 'text-[color:var(--color-obsidian)]'"
                      >{{ variant.stock }}</span>
                      <span v-if="variant.stock === 0" class="text-xs text-red-500">Out of stock</span>
                    </span>
                    <input
                      v-else
                      v-model.number="variant.draftStock"
                      type="number"
                      min="0"
                      class="w-20 text-right border border-[color:var(--color-obsidian)] rounded-[var(--radius-sm)] px-2 py-1 text-sm focus:outline-none"
                    />
                  </td>
                  <td class="px-5 py-3 text-right">
                    <span v-if="!variant.editing" class="flex items-center justify-end gap-2">
                      <button
                        class="text-xs text-[color:var(--color-border-strong)] hover:text-[color:var(--color-obsidian)] transition-colors uppercase tracking-wider"
                        @click="startEdit(variant)"
                      >Edit</button>
                    </span>
                    <span v-else class="flex items-center justify-end gap-2">
                      <button
                        class="text-xs text-[color:var(--color-border-strong)] hover:text-[color:var(--color-obsidian)] transition-colors uppercase tracking-wider"
                        @click="cancelEdit(variant)"
                      >Cancel</button>
                      <button
                        class="text-xs bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] px-2.5 py-1 rounded-[var(--radius-sm)] hover:opacity-80 transition-opacity flex items-center gap-1.5"
                        :disabled="saving === variant.id"
                        @click="saveStock(variant)"
                      >
                        <span v-if="saving === variant.id" class="w-2.5 h-2.5 border border-current border-t-transparent rounded-full animate-spin" />
                        Save
                      </button>
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </Transition>
      </div>

      <p v-if="filtered.length === 0" class="text-sm text-[color:var(--color-border-strong)] py-8 text-center">
        No products match "{{ search }}"
      </p>
    </div>
  </div>
</template>

<style scoped>
.variants-expand-enter-active { transition: max-height var(--duration-normal) var(--ease-out-expo), opacity var(--duration-normal) ease; overflow: hidden; }
.variants-expand-leave-active { transition: max-height var(--duration-fast) ease, opacity var(--duration-fast) ease; overflow: hidden; }
.variants-expand-enter-from, .variants-expand-leave-to { max-height: 0; opacity: 0; }
.variants-expand-enter-to, .variants-expand-leave-from { max-height: 600px; opacity: 1; }
</style>
