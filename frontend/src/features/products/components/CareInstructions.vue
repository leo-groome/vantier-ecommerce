<script setup lang="ts">
export interface CareData {
  wash: string
  iron: string
  store: string
  material: string
}

defineProps<{
  lineName: string
  care: CareData
}>()

const CARE_ICONS = {
  wash:     { symbol: '≋', label: 'Lavado'     },
  iron:     { symbol: '◻', label: 'Planchado'  },
  store:    { symbol: '∩', label: 'Almacenaje' },
  material: { symbol: '⊞', label: 'Material'   },
} as const
</script>

<template>
  <section class="bg-[color:var(--color-warm-beige-dk)] py-16 px-[var(--spacing-container)] border-t border-[color:var(--color-obsidian)]/6">
    <div class="max-w-[var(--container-max)] mx-auto">

      <!-- Header -->
      <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] text-[color:var(--color-obsidian)]/35 mb-2">
        {{ lineName }}
      </p>
      <h2 class="text-[length:var(--text-headline)] font-light uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-obsidian)] mb-3">
        Cómo cuidar tu prenda
      </h2>
      <div class="w-7 h-px bg-[color:var(--color-amber-accent)] mb-12" />

      <!-- 4 care items -->
      <div class="grid grid-cols-2 md:grid-cols-4 divide-y md:divide-y-0 md:divide-x divide-[color:var(--color-obsidian)]/6">
        <div
          v-for="(icon, key) in CARE_ICONS"
          :key="key"
          class="p-8 text-center"
          data-care-item
        >
          <!-- Square icon border -->
          <div class="w-9 h-9 mx-auto mb-4 border border-[color:var(--color-obsidian)]/15 flex items-center justify-center">
            <span class="text-base text-[color:var(--color-obsidian)]/35">{{ icon.symbol }}</span>
          </div>
          <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-obsidian)]/55 mb-2">
            {{ icon.label }}
          </p>
          <p class="text-[length:var(--text-micro)] text-[color:var(--color-obsidian)]/38 leading-relaxed">
            {{ care[key] }}
          </p>
        </div>
      </div>

      <!-- Closing tagline -->
      <div class="mt-10 pt-8 border-t border-[color:var(--color-obsidian)]/6 flex items-center gap-4">
        <div class="w-5 h-px bg-[color:var(--color-amber-accent)] flex-shrink-0" />
        <p class="text-[length:var(--text-micro)] text-[color:var(--color-obsidian)]/35 leading-relaxed">
          Una prenda bien cuidada dura décadas. Esto no es moda de temporada — es una inversión en tu guardarropa permanente.
        </p>
      </div>
    </div>
  </section>
</template>
