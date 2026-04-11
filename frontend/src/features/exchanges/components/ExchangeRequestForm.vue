<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{ orderId: string; variantId: string }>()
const emit = defineEmits<{ (e: 'submit', data: { reason: string; preferredVariant: string }): void; (e: 'cancel'): void }>()

const reason = ref('')
const preferredVariant = ref('')
const submitting = ref(false)

const reasons = [
  'Wrong size',
  'Wrong color',
  'Defective item',
  'Changed my mind',
  'Other',
]

async function submit() {
  if (!reason.value || submitting.value) return
  submitting.value = true
  // TODO: wire to exchanges API
  await new Promise((r) => setTimeout(r, 500))
  emit('submit', { reason: reason.value, preferredVariant: preferredVariant.value })
  submitting.value = false
}
</script>

<template>
  <div class="space-y-4">
    <h3 class="text-[length:var(--text-title)] font-semibold text-[color:var(--color-on-surface)]">Request Exchange</h3>
    <p class="text-[length:var(--text-small)] text-[color:var(--color-border-strong)]">
      Order #{{ orderId.slice(-8).toUpperCase() }} · Variant {{ variantId.slice(-6) }}
    </p>

    <div class="space-y-1">
      <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)]">Reason</label>
      <select
        v-model="reason"
        class="w-full border border-[color:var(--color-border)] bg-transparent px-3 py-2.5 text-[length:var(--text-small)] text-[color:var(--color-on-surface)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)]"
      >
        <option value="" disabled>Select a reason</option>
        <option v-for="r in reasons" :key="r" :value="r">{{ r }}</option>
      </select>
    </div>

    <div class="space-y-1">
      <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)]">Preferred Variant (optional)</label>
      <input
        v-model="preferredVariant"
        type="text"
        placeholder="e.g. Size M, Navy"
        class="w-full border border-[color:var(--color-border)] bg-transparent px-3 py-2.5 text-[length:var(--text-small)] text-[color:var(--color-on-surface)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)]"
      />
    </div>

    <div class="flex gap-3 pt-2">
      <button
        :disabled="!reason || submitting"
        class="flex-1 py-3 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-[length:var(--text-small)] tracking-[var(--tracking-label)] uppercase hover:opacity-80 disabled:opacity-40 transition-opacity duration-[var(--duration-normal)] flex items-center justify-center gap-2"
        @click="submit"
      >
        <span v-if="submitting" class="w-4 h-4 border-2 border-[color:var(--color-ivory)] border-t-transparent rounded-full animate-spin" />
        Submit Exchange
      </button>
      <button
        class="px-6 py-3 border border-[color:var(--color-border)] text-[length:var(--text-small)] uppercase tracking-[var(--tracking-label)] hover:border-[color:var(--color-border-strong)] transition-colors duration-[var(--duration-fast)]"
        @click="emit('cancel')"
      >
        Cancel
      </button>
    </div>
  </div>
</template>
