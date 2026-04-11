<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { useProductsStore } from '../store'
import { useCartStore } from '@features/cart/store'
import { useToast } from '@shared/composables/useToast'
import ProductImageGallery from './ProductImageGallery.vue'
import VariantSelector from './VariantSelector.vue'
import SizeGuideModal from './SizeGuideModal.vue'
import SeoHead from '@shared/components/SeoHead.vue'

type AddState = 'idle' | 'loading' | 'success'

const route = useRoute()
const products = useProductsStore()
const cart = useCartStore()
const toast = useToast()

const selectedColor = ref('')
const selectedSize = ref('')
const addState = ref<AddState>('idle')
const sizeGuideOpen = ref(false)
const variantSelector = ref<InstanceType<typeof VariantSelector> | null>(null)

const product = computed(() => products.selected)

// Mock data for when the API isn't wired yet
const MOCK_PRODUCT = {
  id: 'mock-1',
  name: 'Polo Atelier — Classic',
  line: 'Polo Atelier' as const,
  style: 'Classic' as const,
  priceUSD: 180,
  description: 'Crafted from 100% Pima cotton with a refined silhouette. The Classic polo is the cornerstone of the Polo Atelier line — architectural in construction, restrained in detail.',
  images: [
    { id: 'i1', url: '/images/product-polo-1.jpg', alt: 'Polo Atelier Classic — Front', isPrimary: true },
    { id: 'i2', url: '/images/product-polo-2.jpg', alt: 'Polo Atelier Classic — Back', isPrimary: false },
    { id: 'i3', url: '/images/product-polo-3.jpg', alt: 'Polo Atelier Classic — Detail', isPrimary: false },
  ],
  variants: [
    { id: 'v-ivory-s',  size: 'S',  color: 'Ivory',   stock: 12, sku: 'PA-CL-IVY-S'  },
    { id: 'v-ivory-m',  size: 'M',  color: 'Ivory',   stock: 8,  sku: 'PA-CL-IVY-M'  },
    { id: 'v-ivory-l',  size: 'L',  color: 'Ivory',   stock: 3,  sku: 'PA-CL-IVY-L'  },
    { id: 'v-ivory-xl', size: 'XL', color: 'Ivory',   stock: 0,  sku: 'PA-CL-IVY-XL' },
    { id: 'v-obs-s',    size: 'S',  color: 'Obsidian', stock: 15, sku: 'PA-CL-OBS-S'  },
    { id: 'v-obs-m',    size: 'M',  color: 'Obsidian', stock: 10, sku: 'PA-CL-OBS-M'  },
    { id: 'v-obs-l',    size: 'L',  color: 'Obsidian', stock: 5,  sku: 'PA-CL-OBS-L'  },
    { id: 'v-obs-xl',   size: 'XL', color: 'Obsidian', stock: 2,  sku: 'PA-CL-OBS-XL' },
  ],
}

// Use real product from store if available, else mock
const displayProduct = computed(() => product.value ?? MOCK_PRODUCT)

// Auto-select first available color on load
onMounted(async () => {
  try {
    await products.loadProduct(route.params.id as string)
  } catch {
    // API not wired — use mock data
  }
  const firstColor = displayProduct.value.variants[0]?.color
  if (firstColor) selectedColor.value = firstColor
})

function formatPrice(n: number) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n)
}

const resolvedVariant = computed(() => variantSelector.value?.resolvedVariant ?? null)

const canAdd = computed(() =>
  !!selectedColor.value && !!selectedSize.value && !!resolvedVariant.value
)

async function addToCart() {
  if (!canAdd.value || addState.value !== 'idle') return
  addState.value = 'loading'
  await new Promise((r) => setTimeout(r, 350))
  cart.addItem({
    productId: displayProduct.value.id,
    variantId: resolvedVariant.value!.id,
    name: displayProduct.value.name,
    size: selectedSize.value,
    color: selectedColor.value,
    priceUSD: displayProduct.value.priceUSD,
    quantity: 1,
  })
  addState.value = 'success'
  toast.show('Added to cart', 'success')
  setTimeout(() => (addState.value = 'idle'), 1800)
}
</script>

<template>
  <SeoHead
    :title="`${displayProduct.name} — ${displayProduct.line} | Vantier`"
    :description="`${displayProduct.name}. ${displayProduct.line} line. Free shipping on 5+ items.`"
    og-type="product"
  />

  <!-- Breadcrumb -->
  <nav class="max-w-[var(--container-max)] mx-auto px-[var(--spacing-container)] pt-6 pb-2">
    <ol class="flex items-center gap-2 text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-border-strong)]">
      <li><RouterLink to="/" class="hover:text-[color:var(--color-obsidian)] transition-colors">Home</RouterLink></li>
      <li class="opacity-40">/</li>
      <li><RouterLink to="/shop" class="hover:text-[color:var(--color-obsidian)] transition-colors">Shop</RouterLink></li>
      <li class="opacity-40">/</li>
      <li class="text-[color:var(--color-obsidian)]">{{ displayProduct.name }}</li>
    </ol>
  </nav>

  <!-- Main PDP grid -->
  <section class="max-w-[var(--container-max)] mx-auto px-[var(--spacing-container)] py-8">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 xl:gap-20">

      <!-- Left: image gallery -->
      <ProductImageGallery :images="displayProduct.images" />

      <!-- Right: product info -->
      <div class="flex flex-col gap-6 lg:pt-4">

        <!-- Line + style label -->
        <div>
          <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-border-strong)]">
            {{ displayProduct.line }} — {{ displayProduct.style }}
          </p>
          <h1 class="mt-1 text-[length:var(--text-headline)] font-semibold tracking-[var(--tracking-headline)] text-[color:var(--color-on-surface)] uppercase leading-tight">
            {{ displayProduct.name }}
          </h1>
        </div>

        <!-- Price -->
        <p class="text-[length:var(--text-title)] font-light text-[color:var(--color-on-surface)]">
          {{ formatPrice(displayProduct.priceUSD) }}
        </p>

        <!-- Variant selector -->
        <VariantSelector
          ref="variantSelector"
          :variants="displayProduct.variants"
          v-model:selectedColor="selectedColor"
          v-model:selectedSize="selectedSize"
        />

        <!-- Size guide link -->
        <button
          class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] underline text-[color:var(--color-border-strong)] hover:text-[color:var(--color-obsidian)] transition-colors w-fit"
          @click="sizeGuideOpen = true"
        >
          Size Guide
        </button>

        <!-- Add to cart CTA -->
        <div class="space-y-3 pt-2">
          <button
            :disabled="!canAdd || addState !== 'idle'"
            class="w-full py-4 flex items-center justify-center gap-3 text-[length:var(--text-small)] tracking-[var(--tracking-label)] uppercase font-medium transition-all duration-[var(--duration-normal)]"
            :class="[
              addState === 'success'
                ? 'bg-green-900 text-white'
                : 'bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] hover:opacity-80 disabled:opacity-35 disabled:cursor-not-allowed'
            ]"
            @click="addToCart"
          >
            <!-- Loading spinner -->
            <span
              v-if="addState === 'loading'"
              class="w-4 h-4 border-2 border-[color:var(--color-ivory)] border-t-transparent rounded-full animate-spin"
            />
            <!-- Success checkmark -->
            <svg v-else-if="addState === 'success'" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            <span>
              {{ addState === 'success' ? 'Added to Cart' : addState === 'loading' ? 'Adding…' : !selectedColor ? 'Select a Color' : !selectedSize ? 'Select a Size' : 'Add to Cart' }}
            </span>
          </button>

          <!-- Free shipping note -->
          <p class="text-center text-[length:var(--text-micro)] text-[color:var(--color-border-strong)]">
            Free shipping on 5+ items
          </p>
        </div>

        <!-- Description -->
        <div class="border-t border-[color:var(--color-border)] pt-6">
          <p class="text-[length:var(--text-small)] leading-relaxed text-[color:var(--color-border-strong)]">
            {{ (displayProduct as any).description ?? '' }}
          </p>
        </div>

        <!-- Exchange policy -->
        <div class="border-t border-[color:var(--color-border)] pt-4 text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-border-strong)] space-y-1">
          <p>Same-line exchanges · No returns</p>
          <p>Ships within 3–5 business days</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Sticky Add to Cart — mobile only (shown at bottom on small screens) -->
  <Teleport to="body">
    <div
      v-if="!canAdd || addState !== 'success'"
      class="lg:hidden fixed bottom-0 left-0 right-0 z-40 bg-[color:var(--color-surface)] border-t border-[color:var(--color-border)] px-4 py-3 flex items-center gap-3"
    >
      <div class="flex-1">
        <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-border-strong)]">{{ displayProduct.name }}</p>
        <p class="text-[length:var(--text-small)] font-medium">{{ formatPrice(displayProduct.priceUSD) }}</p>
      </div>
      <button
        :disabled="!canAdd || addState !== 'idle'"
        class="px-6 py-3 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-[length:var(--text-small)] tracking-[var(--tracking-label)] uppercase hover:opacity-80 disabled:opacity-35 transition-opacity duration-[var(--duration-fast)] flex items-center gap-2"
        @click="addToCart"
      >
        <span v-if="addState === 'loading'" class="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" />
        {{ addState === 'loading' ? 'Adding…' : 'Add to Cart' }}
      </button>
    </div>
  </Teleport>

  <!-- Size guide modal -->
  <SizeGuideModal :open="sizeGuideOpen" @close="sizeGuideOpen = false" />
</template>
