<script setup lang="ts">
defineProps<{
  lineName: string
  images?: Array<{ src: string; alt: string }>
}>()
</script>

<template>
  <section class="bg-[color:var(--color-warm-beige)] py-16 px-[var(--spacing-container)]">
    <div class="max-w-[var(--container-max)] mx-auto">

      <!-- Header -->
      <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] text-[color:var(--color-obsidian)]/35 mb-2">
        {{ lineName }}
      </p>
      <h2 class="text-[length:var(--text-headline)] font-light uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-obsidian)] mb-3">
        Lookbook
      </h2>
      <div class="w-7 h-px bg-[color:var(--color-amber-accent)] mb-10" />

      <!-- Photo grid: 3:2 main + 2:3 portrait -->
      <div v-if="images && images.length" class="grid grid-cols-3 gap-2 mb-8">
        <div class="col-span-2 aspect-[4/5] overflow-hidden bg-[color:var(--color-obsidian)]">
          <img
            :src="images[0].src"
            :alt="images[0].alt"
            class="w-full h-full object-cover hover:scale-[1.03] transition-transform duration-[600ms] ease-[var(--ease-luxury)]"
          />
        </div>
        <div v-if="images[1]" class="col-span-1 aspect-[4/5] overflow-hidden bg-[color:var(--color-obsidian)]/20">
          <img
            :src="images[1].src"
            :alt="images[1].alt"
            class="w-full h-full object-cover hover:scale-[1.03] transition-transform duration-[600ms] ease-[var(--ease-luxury)]"
          />
        </div>
      </div>

      <!-- Placeholder when no images provided -->
      <div v-else class="grid grid-cols-3 gap-2 mb-8">
        <div class="col-span-2 aspect-[4/5] bg-[color:var(--color-obsidian)]/10 flex items-center justify-center">
          <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-obsidian)]/25">
            Editorial — Próximamente
          </p>
        </div>
        <div class="col-span-1 aspect-[4/5] bg-[color:var(--color-obsidian)]/6" />
      </div>

      <!-- CTA -->
      <div class="text-center">
        <RouterLink
          to="/shop"
          class="inline-flex items-center gap-2 border border-[color:var(--color-obsidian)]/20 px-8 py-3 text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-obsidian)]/55 hover:border-[color:var(--color-obsidian)]/50 hover:text-[color:var(--color-obsidian)] transition-all duration-[var(--duration-normal)]"
        >
          Ver lookbook completo
          <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </RouterLink>
      </div>
    </div>
  </section>
</template>
