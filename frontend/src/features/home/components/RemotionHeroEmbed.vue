<script setup lang="ts">
import { ref, onMounted } from 'vue'

defineProps<{ src?: string; poster: string; alt?: string }>()

const videoEl = ref<HTMLVideoElement>()
const reducedMotion = ref(false)
const inView = ref(false)

onMounted(() => {
  reducedMotion.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  const observer = new IntersectionObserver(
    ([entry]) => { if (entry.isIntersecting) { inView.value = true; observer.disconnect() } },
    { threshold: 0.1 }
  )
  if (videoEl.value) observer.observe(videoEl.value)
})
</script>
<template>
  <div class="relative w-full h-full">
    <img
      v-if="reducedMotion || !src"
      :src="poster"
      :alt="alt ?? ''"
      class="w-full h-full object-cover"
      aria-hidden="true"
    />
    <video
      v-else
      ref="videoEl"
      :src="inView ? src : undefined"
      :poster="poster"
      autoplay
      muted
      loop
      playsinline
      preload="metadata"
      class="w-full h-full object-cover"
      aria-hidden="true"
    />
  </div>
</template>
