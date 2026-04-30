<script setup lang="ts">
import { ref } from 'vue'
import HeroSlidesManager from './HeroSlidesManager.vue'
import CollectionsManager from './CollectionsManager.vue'

const tab = ref<'hero' | 'collections'>('hero')
</script>

<template>
  <div class="space-y-6">
    <!-- Tab bar -->
    <div class="flex gap-1 border-b border-black/[0.06]">
      <button
        v-for="t in [{ key: 'hero', label: 'Hero Slides' }, { key: 'collections', label: 'Colecciones' }]"
        :key="t.key"
        class="px-5 py-3 text-[0.78rem] font-semibold uppercase tracking-wide transition-colors relative"
        :style="tab === t.key
          ? { color: 'var(--admin-amber)', borderBottom: '2px solid var(--admin-amber)' }
          : { color: 'var(--admin-text-secondary)', borderBottom: '2px solid transparent' }"
        @click="tab = t.key as 'hero' | 'collections'"
      >
        {{ t.label }}
      </button>
    </div>

    <!-- Tab content -->
    <HeroSlidesManager v-if="tab === 'hero'" />
    <CollectionsManager v-if="tab === 'collections'" />
  </div>
</template>
