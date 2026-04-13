<script setup lang="ts">
import { ref, onMounted } from 'vue'

const revealed = ref(false)
const sectionRef = ref<HTMLElement | null>(null)

onMounted(() => {
  const observer = new IntersectionObserver(
    ([entry]) => { if (entry.isIntersecting) { revealed.value = true; observer.disconnect() } },
    { threshold: 0.2 }
  )
  if (sectionRef.value) observer.observe(sectionRef.value)
})
</script>

<template>
  <section ref="sectionRef" class="w-full flex flex-col md:flex-row overflow-hidden" style="min-height: 520px;">

    <!-- Left: image panel (40%) -->
    <div class="relative md:basis-2/5 h-64 md:h-auto bg-[color:var(--color-obsidian)] overflow-hidden flex-shrink-0">
      <img
        src="/images/Products/signature-blazer-street.jpg"
        alt="Vantier Signature"
        class="absolute inset-0 w-full h-full object-cover opacity-80"
      />
      <!-- Subtle dark gradient on right edge to blend into divider -->
      <div class="absolute inset-y-0 right-0 w-16 bg-gradient-to-r from-transparent to-[color:var(--color-obsidian)]/60 pointer-events-none" />
      <!-- Gold top accent -->
      <div class="absolute top-0 left-0 w-12 h-px bg-[color:var(--color-amber-accent)]" />
    </div>

    <!-- Gold vertical divider (desktop only) -->
    <div class="hidden md:block w-px bg-[color:var(--color-amber-accent)]/20 flex-shrink-0" />

    <!-- Right: text panel (60%) -->
    <div
      class="md:basis-3/5 bg-[color:var(--color-warm-beige)] flex flex-col justify-center px-10 md:px-16 py-16 md:py-20"
      :style="{
        opacity: revealed ? '1' : '0',
        transform: revealed ? 'translateY(0)' : 'translateY(24px)',
        transition: 'opacity 700ms ease, transform 700ms cubic-bezier(0.25, 0.1, 0.1, 1)',
      }"
    >
      <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] opacity-40 mb-8">
        Los Angeles — México
      </p>

      <blockquote class="text-[length:var(--text-headline)] font-light leading-[1.1] tracking-[var(--tracking-headline)] text-[color:var(--color-obsidian)] max-w-lg">
        "We build clothes that don't ask for attention.<br />They command it."
      </blockquote>

      <!-- Gold rule -->
      <div class="w-10 h-px bg-[color:var(--color-amber-accent)] my-8" />

      <div class="flex flex-col gap-1 mb-10">
        <p class="text-[length:var(--text-small)] uppercase tracking-[var(--tracking-label)] font-medium text-[color:var(--color-obsidian)]">
          Silent Evolution.
        </p>
        <p class="text-[length:var(--text-small)] uppercase tracking-[var(--tracking-label)] font-medium text-[color:var(--color-obsidian)] opacity-50">
          Timeless Legacy. Est. 2024
        </p>
      </div>

      <RouterLink
        to="/about"
        class="inline-flex items-center gap-3 text-[length:var(--text-micro)] font-medium uppercase tracking-[var(--tracking-label)] text-[color:var(--color-obsidian)] hover:opacity-50 transition-opacity duration-[var(--duration-normal)] w-fit"
      >
        Explore the brand
        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </RouterLink>
    </div>
  </section>
</template>
