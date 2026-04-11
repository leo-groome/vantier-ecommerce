<script setup lang="ts">
import { computed } from 'vue'
import ImageWithReveal from '@shared/components/ImageWithReveal.vue'

const props = defineProps<{
  line: 'Polo Atelier' | 'Signature' | 'Essential'
  subtitle: string
  imageUrl: string
  href: string
}>()

const lineLabel = computed(() => {
  const map: Record<string, string> = {
    'Polo Atelier': 'Outerwear',
    'Signature': 'Formals',
    'Essential': 'Casual',
  }
  return map[props.line] ?? ''
})
</script>
<template>
  <RouterLink
    :to="href"
    class="group relative overflow-hidden block aspect-[3/4] bg-[color:var(--color-surface-alt)]"
  >
    <ImageWithReveal
      :src="imageUrl"
      :alt="line"
      class="w-full h-full object-cover transition-transform duration-[var(--duration-slow)] ease-[var(--ease-luxury)] group-hover:scale-[1.03]"
    />
    <!-- Overlay -->
    <div class="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent" />
    <!-- Text -->
    <div class="absolute bottom-0 left-0 p-6 text-white">
      <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-75 mb-1">
        {{ lineLabel }}
      </p>
      <h3 class="text-[length:var(--text-title)] font-semibold uppercase tracking-[var(--tracking-headline)]">
        {{ line }}
      </h3>
      <p class="text-[length:var(--text-small)] opacity-75 mt-1">{{ subtitle }}</p>
    </div>
  </RouterLink>
</template>
