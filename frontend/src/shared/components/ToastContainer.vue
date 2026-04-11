<script setup lang="ts">
import { useToast } from '@shared/composables/useToast'

const { toasts, dismiss } = useToast()

const icons = {
  default: '',
  success: '✓',
  error: '✕',
}

const styles = {
  default: 'bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)]',
  success: 'bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)]',
  error:   'bg-red-900 text-white',
}
</script>

<template>
  <Teleport to="body">
    <div
      class="fixed bottom-6 right-6 z-[100] flex flex-col gap-2 pointer-events-none"
      aria-live="polite"
      aria-label="Notifications"
    >
      <TransitionGroup name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          class="flex items-center gap-3 px-5 py-3.5 text-[length:var(--text-small)] tracking-[var(--tracking-label)] uppercase pointer-events-auto cursor-pointer min-w-[240px] max-w-xs shadow-lg"
          :class="styles[toast.variant]"
          @click="dismiss(toast.id)"
        >
          <span v-if="icons[toast.variant]" class="text-xs font-bold opacity-80">
            {{ icons[toast.variant] }}
          </span>
          <span>{{ toast.message }}</span>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<style>
.toast-enter-active {
  transition: opacity var(--duration-normal) var(--ease-out-expo),
              transform var(--duration-normal) var(--ease-out-expo);
}
.toast-leave-active {
  transition: opacity var(--duration-normal) ease,
              transform var(--duration-normal) ease;
}
.toast-enter-from {
  opacity: 0;
  transform: translateY(12px);
}
.toast-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
.toast-move {
  transition: transform var(--duration-normal) var(--ease-out-expo);
}
</style>
