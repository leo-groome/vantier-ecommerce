<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProductsStore } from '../store'
import type { ProductFilters } from '../types'
import ProductGrid from './ProductGrid.vue'
import ProductFiltersPanel from './ProductFilters.vue'
import SeoHead from '@shared/components/SeoHead.vue'

const route = useRoute()
const router = useRouter()
const store = useProductsStore()

const filters = ref<ProductFilters>({
  line: route.query.line as string | undefined,
  style: route.query.style as string | undefined,
  size: route.query.size as string | undefined,
})

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
      <!-- Sidebar -->
      <div class="hidden lg:block w-48 shrink-0">
        <ProductFiltersPanel v-model="filters" />
      </div>
      <!-- Grid -->
      <div class="flex-1 min-w-0">
        <ProductGrid :products="store.catalog" :loading="store.loading" />
      </div>
    </div>
  </div>
</template>
