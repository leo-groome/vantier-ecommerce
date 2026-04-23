<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchShippingRates } from '../api'
import type { ShippingRate } from '../types'

const props = defineProps<{ zip: string; itemCount: number }>()
const emit = defineEmits<{ (e: 'select', rate: ShippingRate): void }>()

const rates = ref<ShippingRate[]>([])
const selected = ref<string | null>(null)
const loading = ref(true)
const error = ref(false)

onMounted(async () => {
  await fetchRates()
})

async function fetchRates() {
  loading.value = true
  error.value = false
  try {
    rates.value = await fetchShippingRates(props.zip, props.itemCount)
    if (rates.value.length > 0) {
      selected.value = rates.value[0].carrier_id
      emit('select', rates.value[0])
    }
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
}

function selectRate(rate: ShippingRate) {
  selected.value = rate.carrier_id
  emit('select', rate)
}

function formatPrice(n: number) {
  return n === 0 ? 'Free' : new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n)
}
</script>

<template>
  <div class="space-y-3">
    <!-- Skeleton loader -->
    <template v-if="loading">
      <div v-for="i in 2" :key="i" class="h-16 bg-[color:var(--color-warm-beige)] animate-pulse" />
    </template>

    <!-- Error -->
    <div v-else-if="error" class="p-4 border border-red-200 text-[length:var(--text-small)] text-red-700">
      Could not fetch shipping rates.
      <button class="underline ml-2" @click="fetchRates">Retry</button>
    </div>

    <!-- Rate cards -->
    <label
      v-else
      v-for="rate in rates"
      :key="rate.carrier_id"
      class="flex items-center justify-between p-4 border cursor-pointer transition-colors duration-[var(--duration-fast)]"
      :class="selected === rate.carrier_id
        ? 'border-[color:var(--color-obsidian)] bg-[color:var(--color-warm-beige)]'
        : 'border-[color:var(--color-border)] hover:border-[color:var(--color-border-strong)]'"
    >
      <div class="flex items-center gap-3">
        <input
          type="radio"
          :value="rate.carrier_id"
          :checked="selected === rate.carrier_id"
          class="accent-[color:var(--color-obsidian)]"
          @change="selectRate(rate)"
        />
        <div>
          <p class="text-[length:var(--text-small)] font-medium text-[color:var(--color-on-surface)]">
            {{ rate.carrier_name }} {{ rate.service }}
          </p>
          <p class="text-[length:var(--text-micro)] text-[color:var(--color-border-strong)]">
            {{ rate.estimated_days }}–{{ rate.estimated_days + 2 }} business days
          </p>
        </div>
      </div>
      <p class="text-[length:var(--text-small)] font-medium text-[color:var(--color-on-surface)]">
        {{ formatPrice(rate.price_usd) }}
      </p>
    </label>
  </div>
</template>
