<script setup lang="ts">
defineProps<{
  name: string
  tagline: string | null
  label: string | null
  price_from: string | null
  image_url: string | null
  link_url: string
  active?: boolean
  faded?: boolean
}>()
</script>

<template>
  <RouterLink
    :to="link_url"
    class="relative flex flex-col justify-end w-full h-full overflow-hidden bg-[color:var(--color-obsidian)]"
    :style="{ opacity: faded ? '0.75' : '1', transition: 'opacity 400ms ease' }"
  >
    <!-- Background photo -->
    <img
      v-if="image_url"
      :src="image_url"
      :alt="name"
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
    <div v-if="label" class="absolute top-6 left-6">
      <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] opacity-60 text-[color:var(--color-ivory)]">
        {{ label }}
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
        {{ name }}
      </h3>

      <p v-if="tagline" class="text-[length:var(--text-small)] mt-1.5 opacity-65 text-[color:var(--color-ivory)]">
        {{ tagline }}
      </p>

      <!-- Price + CTA row — always visible, CTA expands when active -->
      <div class="flex items-center justify-between mt-5 overflow-hidden">
        <span v-if="price_from" class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-50 text-[color:var(--color-ivory)]">
          {{ price_from }}
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
