<script setup lang="ts">
import { useHead } from '@vueuse/head'

const props = defineProps<{
  title: string
  description: string
  canonical?: string
  ogImage?: string
  ogType?: string
  noindex?: boolean
}>()

useHead({
  title: () => props.title,
  meta: [
    { name: 'description', content: () => props.description },
    { property: 'og:title', content: () => props.title },
    { property: 'og:description', content: () => props.description },
    { property: 'og:type', content: () => props.ogType ?? 'website' },
    ...(props.ogImage ? [{ property: 'og:image', content: props.ogImage }] : []),
    { name: 'robots', content: () => props.noindex ? 'noindex, nofollow' : 'index, follow' },
  ],
  link: props.canonical
    ? [{ rel: 'canonical', href: props.canonical }]
    : [],
})
</script>
<template>
  <!-- renderless -->
</template>
