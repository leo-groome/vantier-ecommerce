<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import type { ProductImage } from '../types'

const props = defineProps<{ images: ProductImage[] }>()

const activeIndex = ref(0)
const lightboxOpen = ref(false)
const lightboxIndex = ref(0)

const active = computed(() => props.images[activeIndex.value] ?? null)
const lightboxImage = computed(() => props.images[lightboxIndex.value] ?? null)

// Reset index when image set changes (color switch)
watch(() => props.images, () => {
  activeIndex.value = 0
}, { deep: false })

function selectImage(i: number) { activeIndex.value = i }

function prev() {
  activeIndex.value = (activeIndex.value - 1 + props.images.length) % props.images.length
}
function next() {
  activeIndex.value = (activeIndex.value + 1) % props.images.length
}

function openLightbox(i: number) {
  lightboxIndex.value = i
  lightboxOpen.value = true
}
function closeLightbox() { lightboxOpen.value = false }

function lbPrev() {
  lightboxIndex.value = (lightboxIndex.value - 1 + props.images.length) % props.images.length
}
function lbNext() {
  lightboxIndex.value = (lightboxIndex.value + 1) % props.images.length
}

function onKeyDown(e: KeyboardEvent) {
  if (!lightboxOpen.value) return
  if (e.key === 'Escape') closeLightbox()
  if (e.key === 'ArrowLeft') lbPrev()
  if (e.key === 'ArrowRight') lbNext()
}

onMounted(() => window.addEventListener('keydown', onKeyDown))
onUnmounted(() => window.removeEventListener('keydown', onKeyDown))
</script>

<template>
  <div class="flex flex-col gap-4">
    <!-- Main image -->
    <div
      class="relative overflow-hidden bg-[color:var(--color-warm-beige)] aspect-[3/4] cursor-zoom-in"
      @click="openLightbox(activeIndex)"
    >
      <!-- Direct img — zero opacity tricks, zero skeletons, zero transitions -->
      <img
        v-if="active"
        :key="active.id"
        :src="active.url"
        :alt="active.alt_text ?? ''"
        class="w-full h-full object-cover"
      />

      <!-- No image placeholder -->
      <div v-else class="w-full h-full flex items-center justify-center">
        <span class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-border-strong)]">No image</span>
      </div>

      <!-- Prev / Next -->
      <template v-if="images.length > 1">
        <button
          class="absolute left-3 top-1/2 -translate-y-1/2 w-9 h-9 bg-[color:var(--color-ivory)]/80 backdrop-blur-sm flex items-center justify-center hover:bg-[color:var(--color-ivory)] transition-colors duration-[var(--duration-fast)]"
          aria-label="Previous image"
          @click.stop="prev"
        >
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="15 18 9 12 15 6"/></svg>
        </button>
        <button
          class="absolute right-3 top-1/2 -translate-y-1/2 w-9 h-9 bg-[color:var(--color-ivory)]/80 backdrop-blur-sm flex items-center justify-center hover:bg-[color:var(--color-ivory)] transition-colors duration-[var(--duration-fast)]"
          aria-label="Next image"
          @click.stop="next"
        >
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="9 18 15 12 9 6"/></svg>
        </button>
      </template>

      <!-- Count pill + zoom hint -->
      <div class="absolute bottom-3 left-0 right-0 flex items-center justify-between px-3 pointer-events-none">
        <span class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-ivory)]/60 bg-[color:var(--color-obsidian)]/40 backdrop-blur-sm px-2 py-0.5">
          Tap to zoom
        </span>
        <span v-if="images.length > 1" class="bg-[color:var(--color-obsidian)]/60 text-[color:var(--color-ivory)] text-[10px] tracking-widest px-2 py-0.5">
          {{ activeIndex + 1 }} / {{ images.length }}
        </span>
      </div>
    </div>

    <!-- Thumbnails -->
    <div v-if="images.length > 1" class="flex gap-2 overflow-x-auto pb-1">
      <button
        v-for="(img, i) in images"
        :key="img.id"
        class="flex-shrink-0 w-16 h-20 overflow-hidden transition-[outline] duration-[var(--duration-fast)]"
        :class="i === activeIndex
          ? 'outline outline-2 outline-offset-1 outline-[color:var(--color-obsidian)]'
          : 'outline outline-1 outline-transparent hover:outline-[color:var(--color-border-strong)]'"
        :aria-label="`View image ${i + 1}`"
        @click="selectImage(i)"
      >
        <img :src="img.url" :alt="img.alt_text ?? ''" class="w-full h-full object-cover" />
      </button>
    </div>
  </div>

  <!-- Lightbox -->
  <Teleport to="body">
    <Transition name="lightbox">
      <div
        v-if="lightboxOpen"
        class="fixed inset-0 z-[80] bg-black/95 flex items-center justify-center"
        @click.self="closeLightbox"
      >
        <button
          class="absolute top-5 right-5 w-10 h-10 flex items-center justify-center text-white/60 hover:text-white transition-colors duration-[var(--duration-fast)]"
          aria-label="Close lightbox"
          @click="closeLightbox"
        >
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>

        <img
          v-if="lightboxImage"
          :key="lightboxIndex"
          :src="lightboxImage.url"
          :alt="lightboxImage.alt_text ?? ''"
          class="max-w-[90vw] max-h-[90vh] object-contain select-none"
        />

        <template v-if="images.length > 1">
          <button
            class="absolute left-4 top-1/2 -translate-y-1/2 w-11 h-11 flex items-center justify-center text-white/50 hover:text-white border border-white/10 hover:border-white/30 transition-all duration-[var(--duration-fast)]"
            aria-label="Previous image"
            @click="lbPrev"
          >
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="15 18 9 12 15 6"/></svg>
          </button>
          <button
            class="absolute right-4 top-1/2 -translate-y-1/2 w-11 h-11 flex items-center justify-center text-white/50 hover:text-white border border-white/10 hover:border-white/30 transition-all duration-[var(--duration-fast)]"
            aria-label="Next image"
            @click="lbNext"
          >
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="9 18 15 12 9 6"/></svg>
          </button>
        </template>

        <div class="absolute bottom-5 left-1/2 -translate-x-1/2 text-[length:var(--text-micro)] text-white/40 uppercase tracking-[var(--tracking-display)]">
          {{ lightboxIndex + 1 }} / {{ images.length }}
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.lightbox-enter-active { transition: opacity 200ms ease; }
.lightbox-leave-active { transition: opacity 150ms ease; }
.lightbox-enter-from, .lightbox-leave-to { opacity: 0; }
</style>
