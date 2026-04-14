<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProductsStore } from '../store'
import type { ProductFilters } from '../types'
import ProductGrid from './ProductGrid.vue'
import ProductFiltersPanel from './ProductFilters.vue'
import MobileFilterDrawer from './MobileFilterDrawer.vue'
import SeoHead from '@shared/components/SeoHead.vue'

const route = useRoute()
const router = useRouter()
const store = useProductsStore()

const filters = ref<ProductFilters>({
  line: route.query.line as string | undefined,
  style: route.query.style as string | undefined,
  size: route.query.size as string | undefined,
})

const mobileFilterOpen = ref(false)

// Count active filters for badge
const activeFilterCount = computed(() =>
  Object.values(filters.value).filter(v => v !== undefined && v !== '').length
)

watch(filters, (val) => {
  router.replace({ query: { ...val } })
  store.filters = val
  store.loadCatalog()
}, { deep: true })

onMounted(() => {
  store.filters = filters.value
  store.loadCatalog()
})
</script>

<template>
  <SeoHead
    title="Shop Vantier Menswear — Polo Atelier, Signature, Essential"
    description="Browse the full Vantier collection. Filter by line, style, size, and color."
    canonical="https://vantierluxuryla.com/shop"
  />
  <div class="max-w-[var(--container-max)] mx-auto px-[var(--spacing-container)] py-16">
    <h1 class="text-[length:var(--text-headline)] font-light uppercase tracking-[var(--tracking-headline)] mb-12">
      The Collection
    </h1>
    <div class="flex gap-12">
      <!-- Sidebar (desktop only) -->
      <div class="hidden lg:block w-48 shrink-0">
        <ProductFiltersPanel v-model="filters" />
      </div>
      <!-- Grid -->
      <div class="flex-1 min-w-0">
        <ProductGrid :products="store.catalog" :loading="store.loading" />
      </div>
    </div>
  </div>

  <!-- Mobile filter trigger (sticky bottom, < lg only) -->
  <div class="lg:hidden fixed bottom-6 left-1/2 -translate-x-1/2 z-30">
    <button
      class="flex items-center gap-2.5 px-6 py-3 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-[length:var(--text-micro)] font-medium uppercase tracking-[var(--tracking-label)] shadow-xl hover:opacity-80 transition-opacity duration-[var(--duration-fast)]"
      @click="mobileFilterOpen = true"
    >
      <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3z"/>
      </svg>
      Filter
      <span
        v-if="activeFilterCount > 0"
        class="ml-0.5 w-4 h-4 rounded-full bg-[color:var(--color-amber-accent)] text-[color:var(--color-obsidian)] text-[10px] font-bold flex items-center justify-center"
      >
        {{ activeFilterCount }}
      </span>
    </button>
  </div>

  <!-- Mobile filter drawer (teleported) -->
  <Teleport to="body">
    <MobileFilterDrawer
      v-model="filters"
      :open="mobileFilterOpen"
      @close="mobileFilterOpen = false"
    />
  </Teleport>
</template>
