<script setup lang="ts">
import { ref, onMounted } from 'vue'
import ProductLineCard from './ProductLineCard.vue'
import { fetchCollections, type Collection } from '@/features/home/api'

const hovered = ref<number | null>(null)
const collections = ref<Collection[]>([])

onMounted(async () => {
  try {
    collections.value = await fetchCollections()
  } catch {
    // silently fail — section stays empty
  }
})
</script>

<template>
  <section v-if="collections.length" class="flex w-full overflow-hidden" style="height: 100svh;">
    <div
      v-for="(item, i) in collections"
      :key="item.id"
      class="relative overflow-hidden"
      :style="{
        flex: hovered === null ? '1 1 0' : hovered === i ? '1.9 1 0' : '0.55 1 0',
        transition: 'flex 600ms cubic-bezier(0.25, 0.1, 0.1, 1)',
      }"
      @mouseenter="hovered = i"
      @mouseleave="hovered = null"
    >
      <ProductLineCard
        :name="item.name"
        :tagline="item.tagline"
        :label="item.label"
        :price_from="item.price_from"
        :image_url="item.image_url"
        :link_url="item.link_url"
        :active="hovered === i"
        :faded="hovered !== null && hovered !== i"
      />
    </div>
  </section>
</template>
