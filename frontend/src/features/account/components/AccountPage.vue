<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import AddressCard from './AddressCard.vue'
import type { SavedAddress } from './AddressCard.vue'
import SeoHead from '@shared/components/SeoHead.vue'

const addresses = ref<SavedAddress[]>([
  {
    id: 'addr-1',
    label: 'Home',
    firstName: 'Ricardo',
    lastName: 'Vantier',
    address1: 'Av. Álvaro Obregón 123',
    city: 'Mexico City',
    state: 'CDMX',
    zip: '06700',
    country: 'MX',
    isDefault: true,
  },
])

function deleteAddress(id: string) {
  addresses.value = addresses.value.filter((a) => a.id !== id)
}
function setDefault(id: string) {
  addresses.value = addresses.value.map((a) => ({ ...a, isDefault: a.id === id }))
}
</script>

<template>
  <SeoHead
    title="Account — Vantier"
    description="Manage your account and saved addresses"
    :robots="{ index: false, follow: false }"
  />

  <div class="max-w-3xl mx-auto px-[var(--spacing-container)] py-12 space-y-12">
    <h1 class="text-[length:var(--text-headline)] font-semibold text-[color:var(--color-on-surface)] tracking-[var(--tracking-headline)]">
      Account
    </h1>

    <!-- Quick nav -->
    <div class="flex gap-6 border-b border-[color:var(--color-border)] pb-4">
      <RouterLink
        to="/account/orders"
        class="text-[length:var(--text-small)] uppercase tracking-[var(--tracking-label)] hover:opacity-70 transition-opacity"
      >Orders</RouterLink>
      <RouterLink
        to="/account/exchanges"
        class="text-[length:var(--text-small)] uppercase tracking-[var(--tracking-label)] hover:opacity-70 transition-opacity"
      >Exchanges</RouterLink>
    </div>

    <!-- Saved addresses -->
    <section class="space-y-4">
      <div class="flex items-center justify-between">
        <h2 class="text-[length:var(--text-title)] font-semibold text-[color:var(--color-on-surface)]">Saved Addresses</h2>
        <button
          class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] underline hover:opacity-70 transition-opacity"
        >
          + Add New
        </button>
      </div>

      <div v-if="addresses.length === 0" class="text-[length:var(--text-small)] text-[color:var(--color-border-strong)]">
        No saved addresses.
      </div>
      <div v-else class="space-y-3">
        <AddressCard
          v-for="addr in addresses"
          :key="addr.id"
          :address="addr"
          @edit="() => {}"
          @delete="deleteAddress"
          @set-default="setDefault"
        />
      </div>
    </section>
  </div>
</template>
