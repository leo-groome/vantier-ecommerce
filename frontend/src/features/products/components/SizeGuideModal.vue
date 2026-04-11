<script setup lang="ts">
defineProps<{ open: boolean }>()
const emit = defineEmits<{ (e: 'close'): void }>()

const measurements = [
  { size: 'S',    chest: '36–38"', waist: '29–31"', hip: '36–38"' },
  { size: 'M',    chest: '39–41"', waist: '32–34"', hip: '39–41"' },
  { size: 'L',    chest: '42–44"', waist: '35–37"', hip: '42–44"' },
  { size: 'XL',   chest: '45–47"', waist: '38–40"', hip: '45–47"' },
  { size: 'XXL',  chest: '48–50"', waist: '41–43"', hip: '48–50"' },
  { size: 'XXXL', chest: '51–53"', waist: '44–46"', hip: '51–53"' },
]
</script>

<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div
        v-if="open"
        class="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-4"
        @click.self="emit('close')"
      >
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-[color:var(--color-obsidian)]/40 backdrop-blur-[2px]" @click="emit('close')" />

        <!-- Panel -->
        <div class="relative z-10 bg-[color:var(--color-surface)] w-full max-w-lg p-8">
          <div class="flex items-center justify-between mb-6">
            <div>
              <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-border-strong)] mb-1">Guide</p>
              <h2 class="text-[length:var(--text-title)] font-semibold tracking-[var(--tracking-headline)]">Size Guide</h2>
            </div>
            <button
              class="w-8 h-8 flex items-center justify-center text-[color:var(--color-border-strong)] hover:text-[color:var(--color-obsidian)] transition-colors"
              aria-label="Close size guide"
              @click="emit('close')"
            >
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>

          <p class="text-[length:var(--text-small)] text-[color:var(--color-border-strong)] mb-5">
            Measurements in inches. For best fit, measure your chest at its widest point.
          </p>

          <div class="overflow-x-auto">
            <table class="w-full text-[length:var(--text-small)]">
              <thead>
                <tr class="border-b border-[color:var(--color-border)]">
                  <th class="py-2 pr-6 text-left text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] font-medium text-[color:var(--color-border-strong)]">Size</th>
                  <th class="py-2 pr-6 text-left text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] font-medium text-[color:var(--color-border-strong)]">Chest</th>
                  <th class="py-2 pr-6 text-left text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] font-medium text-[color:var(--color-border-strong)]">Waist</th>
                  <th class="py-2 text-left text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] font-medium text-[color:var(--color-border-strong)]">Hip</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="row in measurements"
                  :key="row.size"
                  class="border-b border-[color:var(--color-border)] last:border-0"
                >
                  <td class="py-3 pr-6 font-medium text-[color:var(--color-on-surface)]">{{ row.size }}</td>
                  <td class="py-3 pr-6 text-[color:var(--color-border-strong)]">{{ row.chest }}</td>
                  <td class="py-3 pr-6 text-[color:var(--color-border-strong)]">{{ row.waist }}</td>
                  <td class="py-3 text-[color:var(--color-border-strong)]">{{ row.hip }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity var(--duration-normal) ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>
