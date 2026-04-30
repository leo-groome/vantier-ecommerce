<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'
import { fetchHeroSlides, type HeroSlide } from '@/features/home/api'

const slides = ref<HeroSlide[]>([])
const current = ref(0)
let timer: ReturnType<typeof setInterval> | null = null
const scrollY = ref(0)

function prev() { current.value = (current.value - 1 + slides.value.length) % slides.value.length; restart() }
function next() { current.value = (current.value + 1) % slides.value.length; restart() }
function goTo(i: number) { current.value = i; restart() }
function restart() {
  if (timer) clearInterval(timer)
  timer = setInterval(() => { current.value = (current.value + 1) % slides.value.length }, 6000)
}

function onScroll() {
  scrollY.value = window.scrollY
}

onMounted(async () => {
  window.addEventListener('scroll', onScroll, { passive: true })
  try {
    slides.value = await fetchHeroSlides()
  } catch {
    // silently fail — section stays empty rather than crashing
  }
  if (slides.value.length > 0) {
    timer = setInterval(() => { current.value = (current.value + 1) % slides.value.length }, 6000)
  }
})
onUnmounted(() => {
  if (timer) clearInterval(timer)
  window.removeEventListener('scroll', onScroll)
})
</script>

<template>
  <section class="relative w-full h-screen min-h-[560px] overflow-hidden select-none bg-[color:var(--color-obsidian)]">
    <TransitionGroup name="hero-slide">
      <div
        v-for="(slide, i) in slides"
        v-show="i === current"
        :key="slide.id"
        class="absolute inset-0 flex flex-col justify-end"
        :class="slide.theme === 'dark' ? 'bg-[color:var(--color-obsidian)]' : 'bg-[color:var(--color-ivory)]'"
      >
        <!-- Background photo -->
        <img
          v-if="slide.image_url"
          :src="slide.image_url"
          :alt="slide.subtitle ?? slide.title"
          class="absolute inset-0 w-full h-full object-cover pointer-events-none"
          :class="slide.theme === 'dark' ? 'opacity-60' : 'opacity-45'"
          :style="{ objectPosition: `50% calc(50% + ${scrollY * 0.15}px)` }"
        />
        <!-- Architectural lines -->
        <div
          class="absolute top-0 left-0 w-px h-full opacity-10"
          :class="slide.theme === 'dark' ? 'bg-[color:var(--color-ivory)]' : 'bg-[color:var(--color-obsidian)]'"
        />
        <div
          class="absolute top-0 right-[38%] w-px h-full opacity-[0.04]"
          :class="slide.theme === 'dark' ? 'bg-[color:var(--color-ivory)]' : 'bg-[color:var(--color-obsidian)]'"
        />

        <!-- Content -->
        <div
          class="relative z-10 pb-20 px-[var(--spacing-container)] max-w-[var(--container-max)] mx-auto w-full"
          :style="{
            transform: `translateY(${scrollY * 0.12}px)`,
            opacity: Math.max(0, 1 - scrollY / 380),
          }"
        >
          <p
            class="text-[length:var(--text-micro)] font-medium uppercase tracking-[var(--tracking-display)] mb-8 opacity-40"
            :class="slide.theme === 'dark' ? 'text-[color:var(--color-ivory)]' : 'text-[color:var(--color-obsidian)]'"
          >{{ slide.label }}</p>

          <h1
            class="text-[length:var(--text-display)] font-light uppercase tracking-[var(--tracking-headline)] leading-[1.0] whitespace-pre-line max-w-3xl"
            :class="slide.theme === 'dark' ? 'text-[color:var(--color-ivory)]' : 'text-[color:var(--color-obsidian)]'"
          >{{ slide.title }}</h1>

          <!-- Gold accent line -->
          <div v-if="slide.subtitle" class="mt-6 flex items-center gap-5">
            <div class="w-10 h-px bg-[color:var(--color-amber-accent)]" />
            <p
              class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-50"
              :class="slide.theme === 'dark' ? 'text-[color:var(--color-ivory)]' : 'text-[color:var(--color-obsidian)]'"
            >{{ slide.subtitle }}</p>
          </div>

          <RouterLink
            :to="slide.cta_url"
            class="mt-10 inline-flex items-center gap-3 text-[length:var(--text-small)] font-medium uppercase tracking-[var(--tracking-label)] transition-opacity duration-[var(--duration-normal)] hover:opacity-60"
            :class="slide.theme === 'dark' ? 'text-[color:var(--color-ivory)]' : 'text-[color:var(--color-obsidian)]'"
          >
            {{ slide.cta_text }}
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </RouterLink>
        </div>

        <!-- Slide counter -->
        <div
          class="absolute bottom-8 right-[var(--spacing-container)] text-[length:var(--text-micro)] font-mono opacity-30"
          :class="slide.theme === 'dark' ? 'text-[color:var(--color-ivory)]' : 'text-[color:var(--color-obsidian)]'"
        >{{ String(i + 1).padStart(2, '0') }} / {{ String(slides.length).padStart(2, '0') }}</div>
      </div>
    </TransitionGroup>

    <!-- Gold progress bar -->
    <div class="absolute bottom-0 left-0 right-0 h-px bg-white/10 z-20">
      <div
        class="h-full bg-[color:var(--color-amber-accent)] transition-[width] duration-[600ms] ease-linear"
        :style="{ width: slides.length ? `${((current + 1) / slides.length) * 100}%` : '0%' }"
      />
    </div>

    <!-- Prev / Next -->
    <button
      v-if="slides.length > 1"
      class="absolute left-6 top-1/2 -translate-y-1/2 z-20 w-10 h-10 flex items-center justify-center border border-white/20 hover:border-[color:var(--color-amber-accent)] text-white transition-colors duration-[var(--duration-fast)]"
      aria-label="Previous"
      @click="prev"
    >
      <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M19 12H5M12 19l-7-7 7-7" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
    <button
      v-if="slides.length > 1"
      class="absolute right-6 top-1/2 -translate-y-1/2 z-20 w-10 h-10 flex items-center justify-center border border-white/20 hover:border-[color:var(--color-amber-accent)] text-white transition-colors duration-[var(--duration-fast)]"
      aria-label="Next"
      @click="next"
    >
      <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>

    <!-- Dot indicators — gold active -->
    <div v-if="slides.length > 1" class="absolute bottom-5 left-1/2 -translate-x-1/2 z-20 flex items-center gap-2">
      <button
        v-for="(_, i) in slides"
        :key="i"
        class="transition-all duration-[var(--duration-normal)]"
        :class="i === current
          ? 'w-6 h-1 bg-[color:var(--color-amber-accent)]'
          : 'w-1 h-1 bg-white/30 hover:bg-white/60 rounded-full'"
        :aria-label="`Slide ${i + 1}`"
        @click="goTo(i)"
      />
    </div>
  </section>
</template>

<style scoped>
.hero-slide-enter-active { transition: opacity var(--duration-cinematic) var(--ease-luxury); }
.hero-slide-leave-active { transition: opacity var(--duration-normal) ease; }
.hero-slide-enter-from, .hero-slide-leave-to { opacity: 0; }
</style>
