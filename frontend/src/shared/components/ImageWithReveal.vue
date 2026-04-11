<script setup lang="ts">
import { ref, onMounted } from 'vue'

const props = defineProps<{
  src: string
  alt: string
  class?: string
}>()

const el = ref<HTMLImageElement>()
const visible = ref(false)

onMounted(() => {
  const observer = new IntersectionObserver(
    ([entry]) => { if (entry.isIntersecting) { visible.value = true; observer.disconnect() } },
    { threshold: 0.1 }
  )
  if (el.value) observer.observe(el.value)
})
</script>
<template>
  <img
    ref="el"
    :src="src"
    :alt="alt"
    loading="lazy"
    :class="[props.class, 'transition-opacity duration-[var(--duration-slow)]', visible ? 'opacity-100' : 'opacity-0']"
  />
</template>
