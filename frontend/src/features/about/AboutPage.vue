<script setup lang="ts">
import SeoHead from '@shared/components/SeoHead.vue'
import SectionLabel from '@shared/components/SectionLabel.vue'
</script>

<template>
  <SeoHead
    title="About Vantier — Silent Luxury Menswear"
    description="Vantier is a silent luxury menswear brand from Los Angeles crafting elevated pieces for the discerning modern man."
    canonical="https://vantierluxuryla.com/about"
  />

  <!-- Hero -->
  <section class="h-[60vh] min-h-[400px] flex items-end bg-[color:var(--color-obsidian)] overflow-hidden relative">
    <div class="absolute top-0 right-[40%] w-px h-full bg-white/8" />
    <div class="absolute top-16 left-0 right-0 h-px bg-white/8" />
    <div class="pb-16 px-[var(--spacing-container)] max-w-[var(--container-max)] mx-auto w-full relative z-10">
      <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] text-white/40 mb-6">
        Los Angeles — México
      </p>
      <h1 class="text-[length:var(--text-display)] font-light uppercase tracking-[var(--tracking-headline)] leading-[1.0] text-[color:var(--color-ivory)] max-w-2xl">
        ABOUT<br />VANTIER
      </h1>
    </div>
  </section>

  <!-- Mission -->
  <section class="py-[var(--spacing-section)]">
    <div class="max-w-[var(--container-max)] mx-auto px-[var(--spacing-container)]">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-start">
        <div>
          <SectionLabel text="The Philosophy" />
          <h2 class="mt-4 text-[length:var(--text-headline)] font-light uppercase tracking-[var(--tracking-headline)] leading-[1.1]">
            Silent luxury.<br />No logos.<br />Only craft.
          </h2>
        </div>
        <div class="space-y-6 text-[length:var(--text-body)] leading-relaxed text-[color:var(--color-on-surface)] opacity-70 lg:pt-12">
          <p>
            Vantier was founded on a single conviction: that true luxury speaks in whispers. In a world saturated with logomania and conspicuous consumption, we chose restraint.
          </p>
          <p>
            Every piece in the Vantier collection is the result of obsessive attention to material and construction — not branding. Our garments are for the man who understands quality without needing to announce it.
          </p>
          <p>
            Based between Los Angeles and México, we operate at the intersection of West Coast ease and Latin American artisanal tradition.
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Three pillars -->
  <section class="py-[var(--spacing-section)] bg-[color:var(--color-warm-beige)]">
    <div class="max-w-[var(--container-max)] mx-auto px-[var(--spacing-container)]">
      <SectionLabel text="The Pillars" />
      <div class="mt-10 grid grid-cols-1 md:grid-cols-3 gap-12">
        <div v-for="pillar in pillars" :key="pillar.title" class="space-y-4">
          <div class="w-8 h-px bg-[color:var(--color-amber-accent)]" />
          <h3 class="text-[length:var(--text-title)] font-semibold uppercase tracking-[var(--tracking-headline)]">{{ pillar.title }}</h3>
          <p class="text-[length:var(--text-small)] leading-relaxed opacity-60">{{ pillar.body }}</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Collections intro -->
  <section class="py-[var(--spacing-section)]">
    <div class="max-w-[var(--container-max)] mx-auto px-[var(--spacing-container)]">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-16">
        <div>
          <SectionLabel text="The Collections" />
          <h2 class="mt-4 text-[length:var(--text-headline)] font-light uppercase tracking-[var(--tracking-headline)] leading-[1.1]">
            Three lines.<br />One language.
          </h2>
        </div>
        <div class="space-y-8 lg:pt-12">
          <div v-for="line in lines" :key="line.name" class="border-b border-[color:var(--color-border)] pb-6">
            <div class="flex items-start justify-between gap-4">
              <div>
                <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-50 mb-1">{{ line.range }}</p>
                <h4 class="font-medium uppercase tracking-[var(--tracking-label)]">{{ line.name }}</h4>
                <p class="mt-2 text-[length:var(--text-small)] opacity-60 leading-relaxed">{{ line.desc }}</p>
              </div>
              <RouterLink
                to="/shop"
                class="flex-shrink-0 text-[length:var(--text-micro)] uppercase tracking-widest opacity-40 hover:opacity-100 transition-opacity duration-[var(--duration-fast)]"
              >Shop →</RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- CTA -->
  <section class="py-20 bg-[color:var(--color-obsidian)] text-center">
    <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] text-white/40 mb-6">Begin here</p>
    <h2 class="text-[length:var(--text-headline)] font-light uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-ivory)] max-w-lg mx-auto px-6">
      Discover the Collection
    </h2>
    <RouterLink
      to="/shop"
      class="mt-10 inline-flex items-center gap-3 text-[length:var(--text-small)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-ivory)] border-b border-white/30 pb-0.5 hover:border-white transition-colors duration-[var(--duration-normal)]"
    >
      Shop All
      <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </RouterLink>
  </section>
</template>

<script lang="ts">
const pillars = [
  {
    title: 'Material',
    body: 'We source exclusively from mills that have mastered their craft over generations — Pima cotton from Peru, Egyptian long-staple from the Nile Delta.',
  },
  {
    title: 'Construction',
    body: 'Every stitch is deliberate. Reinforced seams, collar stays, precision-cut panels. Garments built to outlast seasons, not follow them.',
  },
  {
    title: 'Restraint',
    body: 'No logos. No seasonal trends. No unnecessary ornamentation. The garment itself is the statement — when it needs to make one.',
  },
]

const lines = [
  {
    name: 'Polo Atelier',
    range: 'From $180',
    desc: 'Architectural collar construction, premium Pima cotton. The signature piece of the Vantier wardrobe.',
  },
  {
    name: 'Signature',
    range: 'From $205',
    desc: 'Long-staple Egyptian cotton shirts. Impeccably tailored for presence without effort.',
  },
  {
    name: 'Essential',
    range: 'From $95',
    desc: 'Supima cotton tees with a relaxed silhouette. The everyday foundation of the discerning wardrobe.',
  },
]
</script>
