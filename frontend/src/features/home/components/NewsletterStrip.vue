<script setup lang="ts">
const newsletterUrl = 'https://vantierluxuryla.com/newsletter'
</script>

<template>
  <section class="bg-[color:var(--color-warm-beige-dk)] py-16 px-[var(--spacing-container)] border-y border-[color:var(--color-obsidian)]/6">
    <div class="max-w-[var(--container-max)] mx-auto flex flex-col md:flex-row md:items-center md:justify-between gap-8">

      <!-- Left copy -->
      <div class="shrink-0">
        <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] text-[color:var(--color-obsidian)]/35 mb-2">
          Acceso Exclusivo
        </p>
        <h2 class="text-[length:var(--text-title)] font-light uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-obsidian)]">
          Únete al círculo Vantier
        </h2>
        <p class="mt-2 text-[length:var(--text-micro)] text-[color:var(--color-obsidian)]/45">
          15% en tu primera compra · Acceso early a nuevas colecciones
        </p>
      </div>

      <!-- CTA -->
      <a
        :href="newsletterUrl"
        target="_blank"
        rel="noopener noreferrer"
        data-newsletter-cta
        class="inline-flex items-center gap-3 border border-[color:var(--color-obsidian)] px-8 py-4 text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] text-[color:var(--color-obsidian)] hover:bg-[color:var(--color-obsidian)] hover:text-[color:var(--color-ivory)] transition-colors duration-[var(--duration-normal)] shrink-0"
      >
        Unirme al círculo
        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </a>
    </div>
  </section>
</template>
