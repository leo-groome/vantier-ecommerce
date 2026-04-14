<script setup lang="ts">
import { ref } from 'vue'
import ProductLineCard from './ProductLineCard.vue'

const hovered = ref<number | null>(null)

const lines = [
  { line: 'Polo Atelier' as const, subtitle: 'Structural excellence', href: '/shop' },
  { line: 'Signature'    as const, subtitle: 'Sartorial presence',    href: '/shop' },
  { line: 'Essential'    as const, subtitle: 'Effortless ease',       href: '/shop' },
]
</script>

<template>
  <section class="flex w-full overflow-hidden" style="height: 100svh;">
    <div
      v-for="(item, i) in lines"
      :key="item.line"
      class="relative overflow-hidden"
      :style="{
        flex: hovered === null ? '1 1 0' : hovered === i ? '1.9 1 0' : '0.55 1 0',
        transition: 'flex 600ms cubic-bezier(0.25, 0.1, 0.1, 1)',
      }"
      @mouseenter="hovered = i"
      @mouseleave="hovered = null"
    >
      <ProductLineCard
        :line="item.line"
        :subtitle="item.subtitle"
        :href="item.href"
        :active="hovered === i"
        :faded="hovered !== null && hovered !== i"
      />
    </div>
  </section>
</template>
