<script setup lang="ts">
import { ref, computed } from 'vue'
import type { ProductImage } from '../types'

const props = defineProps<{ images: ProductImage[] }>()

const activeIndex = ref(0)
const active = computed(() => props.images[activeIndex.value] ?? null)

function selectImage(i: number) {
  activeIndex.value = i
}

function prev() {
  activeIndex.value = (activeIndex.value - 1 + props.images.length) % props.images.length
}
function next() {
  activeIndex.value = (activeIndex.value + 1) % props.images.length
}
</script>

<template>
  <div class="flex flex-col gap-4">
    <!-- Main image -->
    <div class="relative overflow-hidden bg-[color:var(--color-warm-beige)] aspect-[3/4]">
      <Transition name="gallery-fade" mode="out-in">
        <img
          v-if="active"
          :key="activeIndex"
          :src="active.url"
          :alt="active.alt"
          class="w-full h-full object-cover"
        />
        <!-- Placeholder when no images -->
        <div
          v-else
          class="w-full h-full flex items-center justify-center"
        >
          <span class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-border-strong)]">No image</span>
        </div>
      </Transition>

      <!-- Prev / Next arrows (only if > 1 image) -->
      <template v-if="images.length > 1">
        <button
          class="absolute left-3 top-1/2 -translate-y-1/2 w-9 h-9 bg-[color:var(--color-ivory)]/80 backdrop-blur-sm flex items-center justify-center hover:bg-[color:var(--color-ivory)] transition-colors duration-[var(--duration-fast)]"
          aria-label="Previous image"
          @click="prev"
        >
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="15 18 9 12 15 6"/></svg>
        </button>
        <button
          class="absolute right-3 top-1/2 -translate-y-1/2 w-9 h-9 bg-[color:var(--color-ivory)]/80 backdrop-blur-sm flex items-center justify-center hover:bg-[color:var(--color-ivory)] transition-colors duration-[var(--duration-fast)]"
          aria-label="Next image"
          @click="next"
        >
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="9 18 15 12 9 6"/></svg>
        </button>
      </template>

      <!-- Image count pill -->
      <div v-if="images.length > 1" class="absolute bottom-3 right-3 bg-[color:var(--color-obsidian)]/60 text-[color:var(--color-ivory)] text-[10px] tracking-widest px-2 py-0.5">
        {{ activeIndex + 1 }} / {{ images.length }}
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
        <img :src="img.url" :alt="img.alt" class="w-full h-full object-cover" />
      </button>
    </div>
  </div>
</template>

<style scoped>
.gallery-fade-enter-active,
.gallery-fade-leave-active {
  transition: opacity var(--duration-normal) var(--ease-luxury);
}
.gallery-fade-enter-from,
.gallery-fade-leave-to {
  opacity: 0;
}
</style>
