<script setup lang="ts">
const steps = [
  {
    number: '01',
    title: 'Diseño',
    body: 'Cada silueta nace de bocetos a mano. Los Angeles define la estructura; México aporta el carácter.',
  },
  {
    number: '02',
    title: 'Confección',
    body: 'Materiales seleccionados pieza por pieza. Costura estructural reforzada. Sin atajos en ninguna etapa.',
  },
  {
    number: '03',
    title: 'Entrega',
    body: 'Empaque minimalista, sin exceso. La prenda llega lista para ser usada. Sin plástico.',
  },
]
</script>

<template>
  <section class="bg-[color:var(--color-obsidian)] py-20 px-[var(--spacing-container)]">
    <div class="max-w-[var(--container-max)] mx-auto">

      <!-- Section header -->
      <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] text-[color:var(--color-amber-accent)]/50 mb-2">
        Vantier
      </p>
      <h2 class="text-[length:var(--text-headline)] font-light uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-ivory)] mb-3">
        El Proceso
      </h2>
      <div class="w-7 h-px bg-[color:var(--color-amber-accent)] mb-12" />

      <!-- Steps grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 divide-y md:divide-y-0 md:divide-x divide-[color:var(--color-amber-accent)]/10">
        <div
          v-for="step in steps"
          :key="step.number"
          class="p-8 md:pl-0 md:pr-8 [&:not(:first-child)]:md:pl-8"
          data-step
        >
          <p
            class="font-mono text-[length:var(--text-micro)] text-[color:var(--color-amber-accent)]/35 tracking-[0.28em] mb-6"
            data-step-number
          >
            {{ step.number }}
          </p>
          <div class="w-5 h-px bg-[color:var(--color-amber-accent)] mb-5" />
          <h3
            class="text-[length:var(--text-small)] font-medium uppercase tracking-[var(--tracking-label)] text-[color:var(--color-ivory)] mb-3"
            data-step-title
          >
            {{ step.title }}
          </h3>
          <p class="text-[length:var(--text-micro)] text-[color:var(--color-ivory)]/35 leading-relaxed">
            {{ step.body }}
          </p>
        </div>
      </div>
    </div>
  </section>
</template>
