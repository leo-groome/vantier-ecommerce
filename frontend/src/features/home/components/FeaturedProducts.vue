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
  <section class="py-[var(--spacing-section)] bg-[color:var(--color-warm-beige)]">
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

        <!-- Editorial 5th tile: spans 2 cols on desktop -->
        <RouterLink
          to="/shop"
          class="relative col-span-2 lg:col-span-2 overflow-hidden bg-[color:var(--color-obsidian)] group"
          style="min-height: 260px;"
        >
          <img
            src="/images/Products/polo-atelier-lifestyle.jpg"
            alt="Polo Atelier Collection"
            class="absolute inset-0 w-full h-full object-cover opacity-55 group-hover:opacity-70 group-hover:scale-[1.03] transition-all duration-[600ms] ease-[cubic-bezier(0.25,0.1,0.1,1)]"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent pointer-events-none" />
          <div class="absolute top-0 left-0 w-8 h-px bg-[color:var(--color-amber-accent)]" />

          <div class="relative z-10 h-full flex flex-col justify-end p-8">
            <div class="w-6 h-px bg-[color:var(--color-amber-accent)] mb-4 group-hover:w-12 transition-[width] duration-[400ms] ease-[cubic-bezier(0.25,0.1,0.1,1)]" />
            <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] opacity-50 text-[color:var(--color-ivory)] mb-1">
              Outerwear
            </p>
            <h3 class="text-[length:var(--text-title)] font-semibold uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-ivory)]">
              The Polo Atelier Collection
            </h3>
            <span class="mt-4 inline-flex items-center gap-2 text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-amber-accent)] opacity-0 group-hover:opacity-100 translate-x-2 group-hover:translate-x-0 transition-all duration-[300ms] ease-out">
              Shop Now
              <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </span>
          </div>
        </RouterLink>
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
