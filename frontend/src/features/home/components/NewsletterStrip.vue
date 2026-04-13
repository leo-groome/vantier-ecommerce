<script setup lang="ts">
// External newsletter signup URL — update when the actual URL is known
const NEWSLETTER_URL = 'https://vantierluxuryla.com/newsletter'
</script>

<template>
  <section class="bg-[color:var(--color-warm-beige-dk)] py-16 px-[var(--spacing-container)] text-center border-y border-[color:var(--color-obsidian)]/6">
    <div class="max-w-[var(--container-max)] mx-auto">

      <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] text-[color:var(--color-obsidian)]/35 mb-3">
        Acceso Exclusivo
      </p>
      <h2 class="text-[length:var(--text-headline)] font-light uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-obsidian)] mb-3">
        Únete al círculo Vantier
      </h2>
      <p class="text-[length:var(--text-small)] text-[color:var(--color-obsidian)]/50 mb-10">
        Suscríbete y recibe 15% de descuento en tu primera compra
      </p>

      <a
        :href="NEWSLETTER_URL"
        target="_blank"
        rel="noopener noreferrer"
        data-newsletter-cta
        class="inline-flex items-center gap-2 border border-[color:var(--color-obsidian)]/20 px-8 py-3.5 text-[length:var(--text-small)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-obsidian)]/60 hover:border-[color:var(--color-obsidian)]/60 hover:text-[color:var(--color-obsidian)] transition-all duration-[var(--duration-normal)]"
      >
        Unirme al círculo
        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </a>
    </div>
  </section>
</template>
