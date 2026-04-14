<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const STORAGE_KEY = 'vantier_announcement_dismissed'

const visible = ref(true)
const activeIndex = ref(0)

const messages = [
  'Free shipping on orders of 5+ items',
  'New arrivals — Polo Atelier S/S 2025',
  'Silent Luxury. Made for LA.',
]

let timer: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  if (localStorage.getItem(STORAGE_KEY) === '1') {
    visible.value = false
    return
  }
  timer = setInterval(() => {
    activeIndex.value = (activeIndex.value + 1) % messages.length
  }, 4000)
})

onUnmounted(() => { if (timer) clearInterval(timer) })

function dismiss() {
  visible.value = false
  localStorage.setItem(STORAGE_KEY, '1')
  if (timer) clearInterval(timer)
}
</script>

<template>
  <Transition name="announcement">
    <div
      v-if="visible"
      class="relative w-full bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] flex items-center justify-center overflow-hidden"
      style="height: 38px;"
    >
      <!-- Rotating messages -->
      <div class="flex-1 flex items-center justify-center overflow-hidden px-10">
        <Transition name="msg-fade" mode="out-in">
          <p
            :key="activeIndex"
            class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-amber-accent)] whitespace-nowrap"
          >
            {{ messages[activeIndex] }}
          </p>
        </Transition>
      </div>

      <!-- Dismiss -->
      <button
        class="absolute right-4 top-1/2 -translate-y-1/2 opacity-40 hover:opacity-100 transition-opacity duration-[var(--duration-fast)] p-1"
        aria-label="Dismiss announcement"
        @click="dismiss"
      >
        <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
      </button>
    </div>
  </Transition>
</template>

<style scoped>
.announcement-leave-active {
  transition: height 300ms var(--ease-luxury), opacity 200ms ease;
  overflow: hidden;
}
.announcement-leave-to {
  height: 0 !important;
  opacity: 0;
}

.msg-fade-enter-active { transition: opacity 300ms ease, transform 300ms var(--ease-luxury); }
.msg-fade-leave-active { transition: opacity 200ms ease, transform 200ms ease; }
.msg-fade-enter-from { opacity: 0; transform: translateY(6px); }
.msg-fade-leave-to   { opacity: 0; transform: translateY(-6px); }
</style>
