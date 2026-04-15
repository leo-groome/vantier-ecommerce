<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchProducts } from '@features/products/api'
import { MOCK_PRODUCTS } from '@features/products/mockData'
import ProductCard from '@features/products/components/ProductCard.vue'
import type { Product } from '@features/products/types'

const featured = ref<Product[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const products = await fetchProducts()
    featured.value = products.slice(0, 4)
    if (featured.value.length === 0) featured.value = MOCK_PRODUCTS.slice(0, 4)
  } catch {
    featured.value = MOCK_PRODUCTS.slice(0, 4)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section class="min-h-screen flex flex-col justify-center py-[var(--spacing-section)] bg-[color:var(--color-warm-beige)]">
    <div class="max-w-[var(--container-max)] mx-auto px-[var(--spacing-container)]">

      <!-- Split header -->
      <div class="flex items-end justify-between mb-3">
        <div>
          <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] opacity-40 mb-2">
            Featured This Season
          </p>
          <h2 class="text-[length:var(--text-headline)] font-light uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-on-surface)]">
            Selected Pieces
          </h2>
        </div>
        <RouterLink
          to="/shop"
          class="hidden sm:inline-flex items-center gap-2 text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-50 hover:opacity-100 transition-opacity duration-[var(--duration-normal)] mb-1"
        >
          View all
          <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </RouterLink>
      </div>

      <!-- Gold divider rule -->
      <div class="w-full h-px bg-[color:var(--color-obsidian)]/10 mb-10" />

      <!-- Skeleton -->
      <div v-if="loading" class="grid grid-cols-2 lg:grid-cols-4 gap-[var(--spacing-card-gap)]">
        <div v-for="i in 4" :key="i" class="aspect-[3/4] bg-[color:var(--color-warm-beige-dk)] animate-pulse" />
      </div>

      <!-- Product grid + editorial card -->
      <div v-else class="grid grid-cols-2 lg:grid-cols-4 gap-[var(--spacing-card-gap)]">
        <ProductCard
          v-for="product in featured"
          :key="product.id"
          :product="product"
        />

      </div>

      <!-- Mobile "View all" -->
      <div class="mt-10 sm:hidden text-center">
        <RouterLink
          to="/shop"
          class="inline-flex items-center gap-3 text-[length:var(--text-small)] uppercase tracking-[var(--tracking-label)] border-b border-[color:var(--color-obsidian)] pb-0.5 hover:opacity-60 transition-opacity duration-[var(--duration-normal)]"
        >
          View Full Collection
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </RouterLink>
      </div>
    </div>
  </section>
</template>
