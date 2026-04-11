<script setup lang="ts">
import { computed, ref } from 'vue'
import type { Product } from '../types'
import ImageWithReveal from '@shared/components/ImageWithReveal.vue'
import EditorialQuote from '@shared/components/EditorialQuote.vue'
import StatusLabel from '@shared/components/StatusLabel.vue'
import ColorSwatch from '@shared/components/ColorSwatch.vue'
import LowStockBadge from './LowStockBadge.vue'

const props = defineProps<{
  product: Product
  status?: string
}>()

const primaryImage = computed(() =>
  props.product.images.find(i => i.isPrimary) ?? props.product.images[0]
)

const uniqueColors = computed(() => {
  const seen = new Set<string>()
  return props.product.variants
    .filter(v => { if (seen.has(v.color)) return false; seen.add(v.color); return true })
    .slice(0, 5)
})

const selectedColor = ref(uniqueColors.value[0]?.color ?? '')

const minStock = computed(() =>
  props.product.variants.reduce((min, v) => Math.min(min, v.stock), Infinity)
)
</script>
<template>
  <article class="group relative flex flex-col">
    <!-- Image container -->
    <RouterLink :to="`/shop/${product.id}`" class="relative overflow-hidden block aspect-[3/4] bg-[color:var(--color-surface-alt)]">
      <ImageWithReveal
        v-if="primaryImage"
        :src="primaryImage.url"
        :alt="primaryImage.alt || product.name"
        class="w-full h-full object-cover transition-transform duration-[var(--duration-slow)] ease-[var(--ease-luxury)] group-hover:scale-[1.03]"
      />
      <!-- Quote overlay — reveals on hover -->
      <div class="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors duration-[var(--duration-normal)] pointer-events-none" />
      <div class="absolute bottom-0 left-0 p-4 opacity-0 group-hover:opacity-100 transition-opacity duration-[var(--duration-normal)] delay-50 translate-y-2 group-hover:translate-y-0 transition-transform">
        <EditorialQuote v-if="product.name" :quote="product.name" />
      </div>
      <!-- Low stock badge -->
      <div class="absolute top-3 left-3">
        <LowStockBadge :stock="minStock" />
      </div>
    </RouterLink>

    <!-- Card info -->
    <div class="mt-3 flex flex-col gap-1.5">
      <StatusLabel
        :category="product.line"
        :status="status ?? product.style"
      />
      <RouterLink :to="`/shop/${product.id}`">
        <h3 class="text-[length:var(--text-small)] font-medium uppercase tracking-[var(--tracking-label)] hover:opacity-70 transition-opacity duration-[var(--duration-fast)]">
          {{ product.name }}
        </h3>
      </RouterLink>
      <p class="text-[length:var(--text-small)] text-[color:var(--color-on-surface)] opacity-60">
        ${{ product.priceUSD.toFixed(2) }} USD
      </p>
      <!-- Color swatches -->
      <div v-if="uniqueColors.length > 0" class="flex gap-1.5 mt-1">
        <ColorSwatch
          v-for="v in uniqueColors"
          :key="v.color"
          :color="v.color"
          :label="v.color"
          :selected="selectedColor === v.color"
          @select="selectedColor = v.color"
        />
      </div>
    </div>
  </article>
</template>
