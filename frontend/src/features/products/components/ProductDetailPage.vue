<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { useProductsStore } from '../store'
import { useCartStore } from '@features/cart/store'
import { useToast } from '@shared/composables/useToast'
import ProductImageGallery from './ProductImageGallery.vue'
import VariantSelector from './VariantSelector.vue'
import SizeGuideModal from './SizeGuideModal.vue'
import ProductCard from './ProductCard.vue'
import SeoHead from '@shared/components/SeoHead.vue'
import { MOCK_PRODUCTS } from '../mockData'
import ProductLookbook from './ProductLookbook.vue'
import CareInstructions from './CareInstructions.vue'
import type { CareData } from './CareInstructions.vue'
import RelatedProducts from './RelatedProducts.vue'

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

// Use real product from store if available, else look up from MOCK_PRODUCTS
const displayProduct = computed(() => {
  if (product.value) return product.value
  const id = route.params.id as string
  return MOCK_PRODUCTS.find(p => p.id === id) ?? MOCK_PRODUCTS[0]
})

// Merge all variants from products in the same line+style so all color swatches show
const allVariants = computed(() => {
  const base = displayProduct.value
  const siblings = MOCK_PRODUCTS.filter(
    p => p.line === base.line && p.style === base.style
  )
  return siblings.flatMap(p => p.variants)
})

// Auto-select first available color on load
onMounted(async () => {
  try {
    await products.loadProduct(route.params.id as string)
  } catch {
    // API not wired — use mock data
  }
  const firstColor = allVariants.value[0]?.color
  if (firstColor) selectedColor.value = firstColor
})


function formatPrice(n: number) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n)
}

const resolvedVariant = computed(() => variantSelector.value?.resolvedVariant ?? null)

// --- Personalization Feature ---
const CUSTOMIZATION_PRICE_USD = 25; // Aprox $450 MXN
const isPersonalized = ref(false)
const custPlacement = ref('')
const custFile = ref<File | null>(null)
const custFilePreview = ref<string>('')

const finalPrice = computed(() => {
  let p = displayProduct.value.priceUSD
  if (isPersonalized.value) p += CUSTOMIZATION_PRICE_USD
  return p
})

function onFileSelect(e: Event) {
  const target = e.target as HTMLInputElement
  if (!target.files?.length) return
  const file = target.files[0]
  if (file.size > 5 * 1024 * 1024) {
    toast.show('El archivo supera los 5MB limit', 'error')
    return
  }
  custFile.value = file
  if (custFilePreview.value) URL.revokeObjectURL(custFilePreview.value)
  custFilePreview.value = URL.createObjectURL(file)
}
// ------------------------------

// Related: same line, different id, max 4
const related = computed(() => {
  const all = products.catalog.length ? products.catalog : MOCK_PRODUCTS
  return all
    .filter(p => p.id !== displayProduct.value.id && p.line === displayProduct.value.line)
    .slice(0, 4)
})

const canAdd = computed(() => {
  if (!selectedColor.value || !selectedSize.value || !resolvedVariant.value) return false
  if (isPersonalized.value && (!custPlacement.value || !custFile.value)) return false
  return true
})

const CARE_BY_LINE: Record<string, CareData> = {
  'Polo Atelier': {
    wash:     'Dry clean solamente',
    iron:     'Temperatura baja, vapor',
    store:    'Colgar, lejos de luz directa',
    material: '100% lana italiana 16 mic',
  },
  'Signature': {
    wash:     'Dry clean o lavado a mano',
    iron:     'Temperatura media, sin vapor directo',
    store:    'Colgar en funda de tela',
    material: '95% algodón Pima, 5% elastano',
  },
  'Essential': {
    wash:     'Lavado a máquina, frío',
    iron:     'Temperatura baja',
    store:    'Doblar, no colgar',
    material: '100% algodón Pima 200g',
  },
}

const RELATED_BY_LINE: Record<string, Array<{ line: string; href: string }>> = {
  'Polo Atelier': [
    { line: 'Signature', href: '/shop?line=signature' },
    { line: 'Essential', href: '/shop?line=essential' },
  ],
  'Signature': [
    { line: 'Polo Atelier', href: '/shop?line=polo-atelier' },
    { line: 'Essential',    href: '/shop?line=essential' },
  ],
  'Essential': [
    { line: 'Polo Atelier', href: '/shop?line=polo-atelier' },
    { line: 'Signature',    href: '/shop?line=signature' },
  ],
}

const currentCare = computed(() => CARE_BY_LINE[displayProduct.value.line] ?? CARE_BY_LINE['Polo Atelier'])
const relatedLines = computed(() => RELATED_BY_LINE[displayProduct.value.line] ?? RELATED_BY_LINE['Polo Atelier'])

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
    priceUSD: finalPrice.value,
    quantity: 1,
    isPersonalized: isPersonalized.value,
    customizationPlacement: custPlacement.value,
    customizationFileUrl: custFilePreview.value,
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
        <p class="text-[length:var(--text-title)] font-light text-[color:var(--color-on-surface)] transition-colors">
          {{ formatPrice(finalPrice) }}
        </p>

        <!-- Variant selector -->
        <VariantSelector
          ref="variantSelector"
          :variants="allVariants"
          v-model:selectedColor="selectedColor"
          v-model:selectedSize="selectedSize"
        />

        <!-- Personalization UI -->
        <div class="border border-[color:var(--color-border)] p-5 mt-2 bg-[#0d0c0a] text-[color:var(--color-ivory)]">
          <div class="flex items-center justify-between cursor-pointer" @click="isPersonalized = !isPersonalized">
            <div>
              <h3 class="text-[length:var(--text-small)] uppercase tracking-[var(--tracking-headline)] font-medium text-[#faf9f6]">
                Personalize Garment
              </h3>
              <p class="text-[length:var(--text-micro)] text-[#faf9f6] opacity-60 mt-1">Upload your design (+{{ formatPrice(CUSTOMIZATION_PRICE_USD) }})</p>
            </div>
            <div class="w-10 h-6 rounded-full border border-[color:var(--color-obsidian)] bg-[#1a1714] p-1 flex items-center transition-all duration-300" :class="{ 'bg-[color:var(--color-obsidian)] border-[color:var(--color-amber-accent)]': isPersonalized }">
              <div class="w-4 h-4 bg-white rounded-full transition-all duration-300 transform" :class="isPersonalized ? 'translate-x-4 bg-[color:var(--color-amber-accent)]' : 'opacity-40'"></div>
            </div>
          </div>

          <div v-if="isPersonalized" class="mt-6 pt-6 border-t border-[color:var(--color-border)]/20 animate-fade-in space-y-5">
            <!-- Placement Selection -->
            <div>
              <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[#faf9f6]/60 mb-3">Placement</p>
              <div class="grid grid-cols-3 gap-3">
                <button
                  v-for="place in ['Chest (Left)', 'Chest (Right)', 'Back']" :key="place"
                  @click="custPlacement = place"
                  class="py-2.5 px-2 border text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] transition-colors text-center"
                  :class="custPlacement === place ? 'border-[color:var(--color-amber-accent)] text-[#faf9f6] bg-[color:var(--color-amber-accent)]/10' : 'border-[#faf9f6]/10 text-[#faf9f6]/40 hover:text-[#faf9f6]/80'"
                >
                  {{ place }}
                </button>
              </div>
            </div>
            
            <!-- File Upload -->
            <div>
              <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[#faf9f6]/60 mb-3">Design File (PNG, SVG)</p>
              <div class="relative border-2 border-dashed border-[#faf9f6]/10 hover:border-[#faf9f6]/30 transition-colors bg-[#1a1714] p-6 text-center cursor-pointer group flex flex-col items-center justify-center min-h-[120px]">
                <input type="file" accept=".png,.svg,.jpg,.jpeg" @change="onFileSelect" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10" />
                
                <template v-if="custFilePreview">
                  <div class="relative mb-3 flex flex-col items-center">
                    <div class="bg-[color:var(--color-amber-accent)]/10 text-[color:var(--color-amber-accent)] w-10 h-10 rounded-full flex items-center justify-center mb-2">
                       <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                         <polyline points="20 6 9 17 4 12"/>
                       </svg>
                    </div>
                    <button class="absolute -top-3 -right-3 sm:-right-8 bg-red-500/20 text-red-500 w-6 h-6 rounded-full flex items-center justify-center shadow-sm hover:bg-red-500/40 transition-colors z-20" @click.stop="[custFile = null, custFilePreview = '']">×</button>
                  </div>
                  <p class="text-[length:var(--text-small)] font-medium text-[#faf9f6]">{{ custFile?.name }}</p>
                  <p class="text-[length:var(--text-micro)] text-[#faf9f6]/40 mt-1">Tap to replace file</p>
                </template>
                <template v-else>
                  <svg class="w-6 h-6 mb-3 text-[#faf9f6]/30 group-hover:text-[color:var(--color-amber-accent)] transition-colors" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <p class="text-[length:var(--text-small)] text-[#faf9f6]/80">Drag and drop or click to upload</p>
                  <p class="text-[length:var(--text-micro)] text-[#faf9f6]/40 mt-1">High-res PNG or SVG • Max 5MB</p>
                </template>
              </div>
            </div>
          </div>
        </div>

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
                ? 'bg-[color:var(--color-obsidian)] text-[color:var(--color-amber-accent)]'
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

  <!-- PDP storytelling sections -->
  <CareInstructions :line-name="displayProduct.line" :care="currentCare" />
  <ProductLookbook :line-name="displayProduct.line" />
  <RelatedProducts :related-lines="relatedLines" />

  <!-- Sticky Add to Cart — mobile only (shown at bottom on small screens) -->
  <Teleport to="body">
    <div
      v-if="!canAdd || addState !== 'success'"
      class="lg:hidden fixed bottom-0 left-0 right-0 z-40 bg-[color:var(--color-surface)] border-t border-[color:var(--color-border)] px-4 py-3 flex items-center gap-3"
    >
      <div class="flex-1">
        <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-border-strong)]">{{ displayProduct.name }}</p>
        <p class="text-[length:var(--text-small)] font-medium">{{ formatPrice(finalPrice) }}</p>
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

  <!-- Related products -->
  <section v-if="related.length" class="bg-[color:var(--color-warm-beige)] py-[var(--spacing-section)]">
    <div class="max-w-[var(--container-max)] mx-auto px-[var(--spacing-container)]">
      <div class="flex items-end justify-between mb-3">
        <div>
          <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] opacity-40 mb-1">{{ displayProduct.line }}</p>
          <h2 class="text-[length:var(--text-title)] font-light uppercase tracking-[var(--tracking-headline)]">You May Also Like</h2>
        </div>
        <RouterLink
          to="/shop"
          class="hidden sm:inline-flex items-center gap-2 text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-40 hover:opacity-100 transition-opacity duration-[var(--duration-normal)] mb-1"
        >
          View all
          <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </RouterLink>
      </div>
      <div class="w-full h-px bg-[color:var(--color-obsidian)]/10 mb-10" />
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-[var(--spacing-card-gap)]">
        <ProductCard v-for="p in related" :key="p.id" :product="p" />
      </div>
    </div>
  </section>
</template>
