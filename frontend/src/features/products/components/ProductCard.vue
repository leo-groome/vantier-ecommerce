<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import type { Product } from '../types'
import { COLOR_BG, COLOR_TEXT } from '../mockData'
import ImageWithReveal from '@shared/components/ImageWithReveal.vue'
import EditorialQuote from '@shared/components/EditorialQuote.vue'
import StatusLabel from '@shared/components/StatusLabel.vue'
import ColorSwatch from '@shared/components/ColorSwatch.vue'
import LowStockBadge from './LowStockBadge.vue'
import { useCartStore } from '@features/cart/store'
import { useToast } from '@shared/composables/useToast'

type QuickState = 'idle' | 'loading' | 'success'

const props = defineProps<{
  product: Product
  status?: string
}>()

const router = useRouter()
const cart = useCartStore()
const toast = useToast()

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

// Quick-add: finds the first in-stock variant for the selected color
// If multiple sizes → navigate to PDP. If exactly one → add directly.
const quickState = ref<QuickState>('idle')

async function onQuickAdd(e: Event) {
  e.preventDefault()
  e.stopPropagation()
  if (quickState.value !== 'idle') return

  const candidates = props.product.variants.filter(
    v => v.color === selectedColor.value && v.stock > 0
  )

  if (candidates.length === 0) {
    toast.show('Out of stock', 'error')
    return
  }

  if (candidates.length > 1) {
    // Multiple sizes — send to PDP to choose
    router.push(`/shop/${props.product.id}`)
    return
  }

  // Exactly one variant — add directly
  quickState.value = 'loading'
  await new Promise(r => setTimeout(r, 300))
  cart.addItem({
    productId: props.product.id,
    variantId: candidates[0].id,
    name: props.product.name,
    size: candidates[0].size,
    color: candidates[0].color,
    priceUSD: props.product.priceUSD,
    quantity: 1,
  })
  quickState.value = 'success'
  toast.show('Added to cart', 'success')
  setTimeout(() => (quickState.value = 'idle'), 1800)
}
</script>

<template>
  <article class="group relative flex flex-col">
    <!-- Image container -->
    <RouterLink :to="`/shop/${product.id}`" class="relative overflow-hidden block aspect-[3/4]">
      <!-- Real product image -->
      <ImageWithReveal
        v-if="primaryImage"
        :src="primaryImage.url"
        :alt="primaryImage.alt || product.name"
        class="w-full h-full object-cover transition-transform duration-[var(--duration-slow)] ease-[var(--ease-luxury)] group-hover:scale-[1.03]"
      />
      <!-- Editorial color placeholder when no image -->
      <div
        v-else
        class="w-full h-full flex flex-col justify-end p-5 transition-transform duration-[var(--duration-slow)] ease-[var(--ease-luxury)] group-hover:scale-[1.03]"
        :style="{ backgroundColor: COLOR_BG[selectedColor] ?? 'oklch(88% 0.018 80)' }"
      >
        <p
          class="text-[length:var(--text-micro)] font-medium uppercase tracking-[var(--tracking-display)] leading-tight max-w-[80%]"
          :style="{ color: COLOR_TEXT[selectedColor] ?? 'oklch(8% 0.005 250)' }"
        >{{ product.name }}</p>
      </div>
      <!-- Quote overlay — reveals on hover -->
      <div class="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors duration-[var(--duration-normal)] pointer-events-none" />
      <div class="absolute bottom-0 left-0 right-0 p-4 flex items-end justify-between">
        <div class="opacity-0 group-hover:opacity-100 transition-opacity duration-[var(--duration-normal)] translate-y-2 group-hover:translate-y-0">
          <EditorialQuote v-if="product.name" :quote="product.name" />
        </div>
        <!-- Quick-add button — visible on hover -->
        <button
          class="opacity-0 group-hover:opacity-100 transition-all duration-[var(--duration-normal)] w-9 h-9 flex items-center justify-center bg-[color:var(--color-ivory)] text-[color:var(--color-obsidian)] hover:bg-[color:var(--color-obsidian)] hover:text-[color:var(--color-ivory)] flex-shrink-0 ml-2"
          :aria-label="`Quick add ${product.name} to cart`"
          @click="onQuickAdd"
        >
          <span v-if="quickState === 'loading'" class="w-3.5 h-3.5 border-2 border-current border-t-transparent rounded-full animate-spin" />
          <svg v-else-if="quickState === 'success'" class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <svg v-else class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
        </button>
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
