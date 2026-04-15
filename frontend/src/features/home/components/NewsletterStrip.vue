<script setup lang="ts">
const newsletterUrl = 'https://lasilentluxury.substack.com/'
</script>

<template>
  <section class="min-h-screen flex flex-col items-center justify-center bg-[color:var(--color-warm-beige-dk)] py-24 px-[var(--spacing-container)] border-y border-[color:var(--color-obsidian)]/6">
    <div class="max-w-2xl mx-auto flex flex-col items-center text-center gap-10">

      <!-- Center copy -->
      <div class="flex flex-col items-center">
        <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] text-[color:var(--color-obsidian)]/40 mb-4 font-medium">
          Acceso Exclusivo
        </p>
        <h2 class="text-[length:var(--text-headline)] md:text-[3.5rem] font-light uppercase tracking-[var(--tracking-headline)] leading-none text-[color:var(--color-obsidian)] mb-6">
          Únete al círculo Vantier
        </h2>
        <div class="w-12 h-px bg-[color:var(--color-obsidian)]/30 mb-6" />
        <p class="text-[length:var(--text-small)] text-[color:var(--color-obsidian)]/60 font-light">
          15% en tu primera compra · Acceso early a nuevas colecciones
        </p>
      </div>

      <!-- CTA -->
      <a
        :href="newsletterUrl"
        target="_blank"
        rel="noopener noreferrer"
        data-newsletter-cta
        class="inline-flex items-center justify-center gap-3 border border-[color:var(--color-obsidian)] px-10 py-5 text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] text-[color:var(--color-obsidian)] hover:bg-[color:var(--color-obsidian)] hover:text-[color:var(--color-ivory)] transition-colors duration-[var(--duration-normal)] shrink-0 w-full md:w-auto mt-2"
      >
        Unirme al círculo
        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </a>
    </div>
  </section>
</template>
