<script setup lang="ts">
const model = defineModel<string>({ default: '' })
</script>

<template>
  <div class="space-y-1">
    <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-on-surface)]">
      Email
    </label>
    <input
      v-model="model"
      type="email"
      placeholder="your@email.com"
      autocomplete="email"
      class="w-full border border-[color:var(--color-border)] bg-transparent px-3 py-2.5 text-[length:var(--text-small)] text-[color:var(--color-on-surface)] placeholder:text-[color:var(--color-border-strong)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)]"
    />
  </div>
</template>
