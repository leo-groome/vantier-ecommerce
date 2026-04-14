<script setup lang="ts">
const props = defineProps<{
  line: 'Polo Atelier' | 'Signature' | 'Essential'
  subtitle: string
  href: string
  active?: boolean
  faded?: boolean
}>()

const DARK: Record<string, boolean> = {
  'Polo Atelier': true,
  'Signature':    false,
  'Essential':    true,
}

const LINE_LABEL: Record<string, string> = {
  'Polo Atelier': 'Outerwear',
  'Signature':    'Formals',
  'Essential':    'Casual',
}

const LINE_PRICE: Record<string, string> = {
  'Polo Atelier': 'From $180',
  'Signature':    'From $205',
  'Essential':    'From $95',
}

const LINE_IMAGE: Record<string, string> = {
  'Polo Atelier': '/images/Products/polo-atelier-jackets-stacked.jpg',
  'Signature':    '/images/Products/signature-shirts-stacked.jpg',
  'Essential':    '/images/Products/essential-blue-tees.jpg',
}

const dark = DARK[props.line]
</script>

<template>
  <RouterLink
    :to="href"
    class="relative flex flex-col justify-end w-full h-full overflow-hidden bg-[color:var(--color-obsidian)]"
    :style="{ opacity: faded ? '0.75' : '1', transition: 'opacity 400ms ease' }"
  >
    <!-- Background photo -->
    <img
      v-if="LINE_IMAGE[line]"
      :src="LINE_IMAGE[line]"
      :alt="line"
      class="absolute inset-0 w-full h-full object-cover"
      :style="{
        opacity: active ? '0.75' : '0.55',
        transform: active ? 'scale(1.04)' : 'scale(1)',
        transition: 'opacity 600ms ease, transform 600ms cubic-bezier(0.25, 0.1, 0.1, 1)',
      }"
    />

    <!-- Gradient overlay — bottom fade for text legibility -->
    <div
      class="absolute inset-0 pointer-events-none"
      :style="{
        background: 'linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.2) 55%, transparent 100%)',
      }"
    />

    <!-- Architectural rule lines -->
    <div class="absolute top-0 right-10 w-px h-full opacity-10 bg-[color:var(--color-ivory)]" />
    <div class="absolute top-14 left-0 right-0 h-px opacity-10 bg-[color:var(--color-ivory)]" />

    <!-- Gold top-left accent -->
    <div class="absolute top-0 left-0 w-8 h-px bg-[color:var(--color-amber-accent)]" />

    <!-- Top label -->
    <div class="absolute top-6 left-6">
      <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] opacity-60 text-[color:var(--color-ivory)]">
        {{ LINE_LABEL[line] }}
      </p>
    </div>

    <!-- Bottom content -->
    <div class="relative z-10 p-7">
      <!-- Gold accent line — grows on active -->
      <div
        class="h-px bg-[color:var(--color-amber-accent)] mb-5"
        :style="{
          width: active ? '3rem' : '1.5rem',
          transition: 'width 400ms cubic-bezier(0.25, 0.1, 0.1, 1)',
        }"
      />

      <h3 class="text-[length:var(--text-title)] font-semibold uppercase tracking-[var(--tracking-headline)] text-[color:var(--color-ivory)]">
        {{ line }}
      </h3>

      <p class="text-[length:var(--text-small)] mt-1.5 opacity-65 text-[color:var(--color-ivory)]">
        {{ subtitle }}
      </p>

      <!-- Price + CTA row — always visible, CTA expands when active -->
      <div class="flex items-center justify-between mt-5 overflow-hidden">
        <span class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-50 text-[color:var(--color-ivory)]">
          {{ LINE_PRICE[line] }}
        </span>

        <span
          class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-amber-accent)] flex items-center gap-1.5"
          :style="{
            opacity: active ? '1' : '0',
            transform: active ? 'translateX(0)' : 'translateX(8px)',
            transition: 'opacity 300ms ease, transform 300ms ease',
          }"
        >
          Shop
          <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </span>
      </div>
    </div>
  </RouterLink>
</template>
