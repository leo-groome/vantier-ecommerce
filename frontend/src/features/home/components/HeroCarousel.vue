<script setup lang="ts">
import { ref } from 'vue'

const slides = [
  {
    label: 'Archival I — Selection 2025',
    heading: 'SILENT EVOLUTION.\nTIMELESS LEGACY.',
    cta: { label: 'Explore the Collection', to: '/shop' },
    imageUrl: '/images/hero-1.jpg',
  },
  {
    label: 'Polo Atelier — Structural Shield',
    heading: 'ARCHITECTURE\nIN MOTION.',
    cta: { label: 'Shop Polo Atelier', to: '/shop?line=polo_atelier' },
    imageUrl: '/images/hero-2.jpg',
  },
]

const current = ref(0)
const prev = () => current.value = (current.value - 1 + slides.length) % slides.length
const next = () => current.value = (current.value + 1) % slides.length
</script>
<template>
  <section class="relative w-full h-[90vh] min-h-[560px] overflow-hidden bg-[color:var(--color-obsidian)]">
    <!-- Slides -->
    <TransitionGroup name="hero-slide">
      <div
        v-for="(slide, i) in slides"
        v-show="i === current"
        :key="i"
        class="absolute inset-0"
      >
        <!-- Background image -->
        <img
          :src="slide.imageUrl"
          :alt="slide.label"
          class="w-full h-full object-cover opacity-60"
        />
        <!-- Overlay gradient -->
        <div class="absolute inset-0 bg-gradient-to-b from-black/20 via-transparent to-black/50" />
      </div>
    </TransitionGroup>

    <!-- Content -->
    <div class="relative z-10 h-full flex flex-col justify-end pb-16 px-[var(--spacing-container)] max-w-[var(--container-max)] mx-auto">
      <p class="text-[length:var(--text-micro)] font-medium uppercase tracking-[var(--tracking-display)] text-white/60 mb-4">
        {{ slides[current].label }}
      </p>
      <h1 class="text-[length:var(--text-display)] font-light uppercase tracking-[var(--tracking-headline)] leading-[var(--leading-tight,1.1)] text-white whitespace-pre-line max-w-2xl">
        {{ slides[current].heading }}
      </h1>
      <RouterLink
        :to="slides[current].cta.to"
        class="mt-8 inline-block text-[length:var(--text-small)] font-medium uppercase tracking-[var(--tracking-label)] text-white border-b border-white/40 pb-0.5 hover:border-white transition-colors duration-[var(--duration-normal)] w-fit"
      >
        {{ slides[current].cta.label }} →
      </RouterLink>
    </div>

    <!-- Navigation -->
    <div class="absolute bottom-8 right-[var(--spacing-container)] z-10 flex items-center gap-4">
      <button @click="prev" aria-label="Previous slide" class="text-white/60 hover:text-white transition-colors duration-[var(--duration-fast)] text-[length:var(--text-small)] uppercase tracking-[var(--tracking-label)]">Prev</button>
      <span class="text-white/30 text-[length:var(--text-micro)]">{{ current + 1 }} / {{ slides.length }}</span>
      <button @click="next" aria-label="Next slide" class="text-white/60 hover:text-white transition-colors duration-[var(--duration-fast)] text-[length:var(--text-small)] uppercase tracking-[var(--tracking-label)]">Next</button>
    </div>

    <!-- Slide transition styles -->
    <style scoped>
    .hero-slide-enter-active,
    .hero-slide-leave-active {
      transition: opacity var(--duration-cinematic) var(--ease-luxury);
    }
    .hero-slide-enter-from,
    .hero-slide-leave-to { opacity: 0; }
    </style>
  </section>
</template>
