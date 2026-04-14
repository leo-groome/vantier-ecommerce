<script setup lang="ts">
defineProps<{
  relatedLines: Array<{ line: string; href: string }>
}>()
</script>

<template>
  <section class="bg-[color:var(--color-warm-beige)] py-16 px-[var(--spacing-container)] border-t border-[color:var(--color-obsidian)]/5">
    <div class="max-w-[var(--container-max)] mx-auto">

      <!-- Header -->
      <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] text-[color:var(--color-obsidian)]/35 mb-2">
        De la misma línea
      </p>
      <h2 class="text-[length:var(--text-headline)] font-light uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-obsidian)] mb-3">
        También te puede interesar
      </h2>
      <div class="w-7 h-px bg-[color:var(--color-amber-accent)] mb-10" />

      <!-- Grid: related cards + shop-all tile -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-[var(--spacing-card-gap)]">

        <!-- Related line cards -->
        <RouterLink
          v-for="item in relatedLines"
          :key="item.line"
          :to="item.href"
          class="relative aspect-[3/4] bg-[color:var(--color-obsidian)]/12 overflow-hidden group"
          data-related-card
        >
          <div class="absolute top-0 left-0 w-6 h-px bg-[color:var(--color-amber-accent)]" />
          <div class="absolute bottom-0 left-0 right-0 p-5 bg-gradient-to-t from-[color:var(--color-obsidian)]/20 to-transparent">
            <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-obsidian)]/45 mb-1">
              Line
            </p>
            <h3 class="text-[length:var(--text-small)] font-medium uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-obsidian)]">
              {{ item.line }}
            </h3>
          </div>
          <div
            class="absolute inset-0 border border-[color:var(--color-obsidian)]/0 group-hover:border-[color:var(--color-amber-accent)]/30 transition-colors duration-[var(--duration-normal)]"
          />
        </RouterLink>

        <!-- Shop all editorial tile -->
        <RouterLink
          to="/shop"
          class="relative aspect-[3/4] bg-[color:var(--color-obsidian)] overflow-hidden flex flex-col items-center justify-center group"
          data-shop-all
        >
          <div class="absolute top-0 left-0 w-5 h-px bg-[color:var(--color-amber-accent)]" />
          <div class="text-center px-6">
            <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] text-[color:var(--color-ivory)]/30 mb-2">Ver toda la</p>
            <h3 class="text-[length:var(--text-title)] font-light tracking-[var(--tracking-headline)] text-[color:var(--color-ivory)]/65 group-hover:text-[color:var(--color-ivory)] transition-colors duration-[var(--duration-normal)]">
              Colección →
            </h3>
          </div>
        </RouterLink>
      </div>
    </div>
  </section>
</template>
