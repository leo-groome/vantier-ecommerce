<script setup lang="ts">
import type { Product } from '../types'
import ProductCard from './ProductCard.vue'

defineProps<{ products: Product[]; loading?: boolean }>()
</script>
<template>
  <div>
    <!-- Skeleton loader -->
    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-[var(--spacing-card-gap)]">
      <div v-for="n in 6" :key="n" class="flex flex-col gap-3">
        <div class="aspect-[3/4] bg-[color:var(--color-surface-alt)] animate-pulse" />
        <div class="h-3 w-24 bg-[color:var(--color-surface-alt)] animate-pulse" />
        <div class="h-4 w-36 bg-[color:var(--color-surface-alt)] animate-pulse" />
        <div class="h-3 w-16 bg-[color:var(--color-surface-alt)] animate-pulse" />
      </div>
    </div>
    <!-- Products -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-[var(--spacing-card-gap)]">
      <ProductCard
        v-for="product in products"
        :key="product.id"
        :product="product"
      />
    </div>
    <!-- Empty state -->
    <div v-if="!loading && products.length === 0" class="py-24 text-center">
      <p class="text-[length:var(--text-small)] uppercase tracking-[var(--tracking-label)] opacity-40">No products found</p>
    </div>
  </div>
</template>
