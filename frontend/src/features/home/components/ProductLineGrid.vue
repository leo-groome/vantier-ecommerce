<script setup lang="ts">
import ProductLineCard from './ProductLineCard.vue'

const lines = [
  {
    line: 'Polo Atelier' as const,
    subtitle: 'Structural excellence',
    imageUrl: '/images/polo-atelier-hero.jpg',
    href: '/shop?line=polo_atelier',
  },
  {
    line: 'Signature' as const,
    subtitle: 'Sartorial presence',
    imageUrl: '/images/signature-hero.jpg',
    href: '/shop?line=signature',
  },
  {
    line: 'Essential' as const,
    subtitle: 'Effortless ease',
    imageUrl: '/images/essential-hero.jpg',
    href: '/shop?line=essential',
  },
]
</script>
<template>
  <section class="py-[var(--spacing-section)]">
    <div class="max-w-[var(--container-max)] mx-auto px-[var(--spacing-container)]">
      <div class="flex items-center gap-4 mb-10">
        <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-50">The Collection</p>
        <div class="flex-1 h-px bg-[color:var(--color-border)]" />
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-[var(--spacing-card-gap)]">
        <ProductLineCard v-for="item in lines" :key="item.line" v-bind="item" />
      </div>
    </div>
  </section>
</template>
