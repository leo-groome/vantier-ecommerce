<script setup lang="ts">
export interface SavedAddress {
  id: string
  label: string
  firstName: string
  lastName: string
  address1: string
  address2?: string
  city: string
  state: string
  zip: string
  country: string
  isDefault: boolean
}

const props = defineProps<{ address: SavedAddress }>()
const emit = defineEmits<{
  (e: 'edit', address: SavedAddress): void
  (e: 'delete', id: string): void
  (e: 'setDefault', id: string): void
}>()
</script>

<template>
  <div
    class="p-5 border transition-colors duration-[var(--duration-fast)]"
    :class="address.isDefault ? 'border-[color:var(--color-obsidian)]' : 'border-[color:var(--color-border)]'"
  >
    <div class="flex items-start justify-between gap-4">
      <div class="space-y-0.5">
        <p class="text-[length:var(--text-small)] font-medium text-[color:var(--color-on-surface)]">
          {{ address.firstName }} {{ address.lastName }}
          <span
            v-if="address.isDefault"
            class="ml-2 text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-border-strong)]"
          >Default</span>
        </p>
        <p class="text-[length:var(--text-small)] text-[color:var(--color-border-strong)]">{{ address.address1 }}</p>
        <p v-if="address.address2" class="text-[length:var(--text-small)] text-[color:var(--color-border-strong)]">{{ address.address2 }}</p>
        <p class="text-[length:var(--text-small)] text-[color:var(--color-border-strong)]">
          {{ address.city }}, {{ address.state }} {{ address.zip }}
        </p>
      </div>
      <div class="flex flex-col gap-1 text-right flex-shrink-0">
        <button
          class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] underline hover:opacity-70 transition-opacity"
          @click="emit('edit', address)"
        >Edit</button>
        <button
          v-if="!address.isDefault"
          class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] underline hover:opacity-70 transition-opacity"
          @click="emit('setDefault', address.id)"
        >Set default</button>
        <button
          class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] underline text-red-600 hover:opacity-70 transition-opacity"
          @click="emit('delete', address.id)"
        >Remove</button>
      </div>
    </div>
  </div>
</template>
