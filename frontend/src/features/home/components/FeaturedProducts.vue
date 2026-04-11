<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Product } from '@features/products/types'
import { fetchProducts } from '@features/products/api'
import ProductCard from '@features/products/components/ProductCard.vue'
import SectionLabel from '@shared/components/SectionLabel.vue'

const featured = ref<Product[]>([])
const loading = ref(true)

// Fallback mock products for when the API isn't available
const MOCK_FEATURED: Product[] = [
  {
    id: 'f1',
    name: 'Polo Atelier — Classic',
    line: 'Polo Atelier',
    style: 'Classic',
    priceUSD: 180,
    description: 'The cornerstone piece. Crafted from 100% Pima cotton.',
    images: [{ id: 'i1', url: '/images/product-polo-1.jpg', alt: 'Polo Atelier Classic', isPrimary: true }],
    variants: [
      { id: 'v1', size: 'S',  color: 'Ivory',    stock: 12, sku: 'PA-CL-IVY-S'  },
      { id: 'v2', size: 'M',  color: 'Ivory',    stock: 8,  sku: 'PA-CL-IVY-M'  },
      { id: 'v3', size: 'S',  color: 'Obsidian', stock: 10, sku: 'PA-CL-OBS-S'  },
      { id: 'v4', size: 'M',  color: 'Obsidian', stock: 6,  sku: 'PA-CL-OBS-M'  },
    ],
  },
  {
    id: 'f2',
    name: 'Signature Shirt',
    line: 'Signature',
    style: 'Design',
    priceUSD: 220,
    description: 'Impeccably tailored. Woven from premium long-staple Egyptian cotton.',
    images: [{ id: 'i2', url: '/images/product-signature-1.jpg', alt: 'Signature Shirt', isPrimary: true }],
    variants: [
      { id: 'v5', size: 'M',  color: 'Midnight', stock: 7,  sku: 'SIG-DS-MID-M'  },
      { id: 'v6', size: 'L',  color: 'Midnight', stock: 4,  sku: 'SIG-DS-MID-L'  },
    ],
  },
  {
    id: 'f3',
    name: 'Essential Tee',
    line: 'Essential',
    style: 'Classic',
    priceUSD: 95,
    description: 'The everyday foundation. Supima cotton, relaxed silhouette.',
    images: [{ id: 'i3', url: '/images/product-essential-1.jpg', alt: 'Essential Tee', isPrimary: true }],
    variants: [
      { id: 'v7', size: 'S',  color: 'Ivory', stock: 20, sku: 'ESS-CL-IVY-S' },
      { id: 'v8', size: 'M',  color: 'Ivory', stock: 15, sku: 'ESS-CL-IVY-M' },
      { id: 'v9', size: 'S',  color: 'Warm Beige', stock: 8, sku: 'ESS-CL-WB-S' },
    ],
  },
  {
    id: 'f4',
    name: 'Polo Atelier — Design',
    line: 'Polo Atelier',
    style: 'Design',
    priceUSD: 195,
    description: 'Architectural collar construction. Contrast stitching detail.',
    images: [{ id: 'i4', url: '/images/product-polo-design-1.jpg', alt: 'Polo Atelier Design', isPrimary: true }],
    variants: [
      { id: 'v10', size: 'M',  color: 'Obsidian', stock: 9,  sku: 'PA-DS-OBS-M' },
      { id: 'v11', size: 'L',  color: 'Obsidian', stock: 3,  sku: 'PA-DS-OBS-L' },
    ],
  },
]

onMounted(async () => {
  try {
    const products = await fetchProducts()
    featured.value = products.slice(0, 4)
    if (featured.value.length === 0) featured.value = MOCK_FEATURED
  } catch {
    featured.value = MOCK_FEATURED
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section class="py-[var(--spacing-section)] bg-[color:var(--color-warm-beige)]">
    <div class="max-w-[var(--container-max)] mx-auto px-[var(--spacing-container)]">
      <!-- Header -->
      <div class="mb-10">
        <SectionLabel text="Featured This Season" />
        <h2 class="mt-3 text-[length:var(--text-headline)] font-semibold uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-on-surface)]">
          Selected Pieces
        </h2>
      </div>

      <!-- Skeleton -->
      <div v-if="loading" class="grid grid-cols-2 lg:grid-cols-4 gap-[var(--spacing-card-gap)]">
        <div v-for="i in 4" :key="i" class="aspect-[3/4] bg-[color:var(--color-warm-beige-dk)] animate-pulse" />
      </div>

      <!-- Product grid -->
      <div v-else class="grid grid-cols-2 lg:grid-cols-4 gap-[var(--spacing-card-gap)]">
        <ProductCard
          v-for="product in featured"
          :key="product.id"
          :product="product"
        />
      </div>
    </div>
  </section>
</template>
