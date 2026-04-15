<script setup lang="ts">
const steps = [
  {
    title: 'The Design',
    body: 'Cada silueta nace de bocetos a mano. Los Ángeles define la estructura anatómica; nuestro legado aporta el carácter intemporal.',
  },
  {
    title: 'The Crafting',
    body: 'Materiales seleccionados pieza por pieza. Costura estructural reforzada terminada a mano. Sin atajos rápidos en ninguna etapa del ensamblaje.',
  },
  {
    title: 'The Delivery',
    body: 'Empaque minimalista, despojado de excesos. La prenda llega lista para ser usada, permitiendo que la arquitectura de la pieza hable por sí sola.',
  },
]
</script>

<template>
  <section class="relative min-h-screen flex flex-col justify-center bg-[color:var(--color-obsidian)] py-28 px-[var(--spacing-container)] border-t border-[color:var(--color-amber-accent)]/10 overflow-hidden">
    <!-- Subtle glow background -->
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top,var(--color-amber-accent)_0%,transparent_70%)] opacity-[0.02] pointer-events-none" />

    <div class="max-w-[var(--container-max)] mx-auto relative z-10">

      <!-- Section header -->
      <div class="flex flex-col items-center text-center mb-24 fade-in-up">
        <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] text-[color:var(--color-amber-accent)] mb-4 font-medium">
          Behind the Garment
        </p>
        <h2 class="text-[length:var(--text-headline)] md:text-[3.5rem] font-light uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-ivory)] leading-none mb-8">
          The Atelier Process
        </h2>
        <div class="w-12 h-px bg-[color:var(--color-amber-accent)]/50" />
      </div>

      <!-- Timeline wrapper -->
      <div class="relative w-full pb-10">
        
        <!-- Horizontal Line (Desktop) -->
        <div class="hidden md:block absolute top-[24px] left-[16.66%] w-[66.66%] h-[1px] bg-[color:var(--color-border-subtle)]">
          <div class="w-0 h-full bg-[color:var(--color-amber-accent)] opacity-50 timeline-line-anim" />
        </div>

        <!-- Vertical Line (Mobile) -->
        <div class="md:hidden absolute top-[24px] bottom-[24px] left-6 w-[1px] bg-[color:var(--color-border-subtle)]"></div>

        <!-- Steps Timeline Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-12 md:gap-8">
          <div
            v-for="(step, index) in steps"
            :key="index"
            class="relative flex flex-row md:flex-col items-start md:items-center text-left md:text-center group"
          >
            
            <!-- Timeline Circle Node -->
            <div class="flex-shrink-0 w-12 h-12 rounded-full border border-[color:var(--color-border-strong)] bg-[color:var(--color-obsidian)] flex items-center justify-center mb-0 md:mb-8 mr-6 md:mr-0 group-hover:border-[color:var(--color-amber-accent)] transition-all duration-700 relative z-10">
              <div class="w-2 h-2 rounded-full bg-[color:var(--color-border-strong)] group-hover:bg-[color:var(--color-amber-accent)] group-hover:shadow-[0_0_10px_var(--color-amber-accent)] transition-all duration-500"></div>
            </div>

            <!-- Content Area -->
            <div class="flex flex-col mt-1 md:mt-0">
              <h3 class="text-[length:var(--text-title)] font-medium uppercase tracking-[var(--tracking-label)] text-[color:var(--color-ivory)] mb-4 group-hover:text-[color:var(--color-amber-accent)] transition-colors duration-500">
                {{ step.title }}
              </h3>
              
              <p class="text-[length:var(--text-small)] text-[color:var(--color-ivory)]/40 leading-[1.8] font-light md:max-w-[280px] lg:max-w-[320px] mx-auto group-hover:text-[color:var(--color-ivory)]/80 transition-colors duration-500">
                {{ step.body }}
              </p>
            </div>

          </div>
        </div>

      </div>
    </div>
  </section>
</template>

<style scoped>
.fade-in-up {
  animation: fadeInUp 1s cubic-bezier(0.25, 0.1, 0.1, 1) forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.timeline-line-anim {
  animation: fillLine 2s cubic-bezier(0.25, 0.1, 0.1, 1) forwards 0.5s;
}

@keyframes fillLine {
  from { width: 0; }
  to { width: 100%; }
}
</style>
