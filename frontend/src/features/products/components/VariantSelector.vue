<script setup lang="ts">
import { computed } from 'vue'
import type { ProductVariant } from '../types'
import ColorSwatch from '@shared/components/ColorSwatch.vue'
import SizeButton from '@shared/components/SizeButton.vue'
import { COLOR_BG } from '../mockData'

const props = defineProps<{
  variants: ProductVariant[]
  selectedColor: string
  selectedSize: string
}>()

const emit = defineEmits<{
  (e: 'update:selectedColor', v: string): void
  (e: 'update:selectedSize', v: string): void
}>()

// Unique colors
const colors = computed(() => [...new Set(props.variants.map((v) => v.color))])

// Sizes available for the selected color (or all if none selected)
const sizes = computed(() => {
  const base = props.selectedColor
    ? props.variants.filter((v) => v.color === props.selectedColor)
    : props.variants
  const unique = [...new Set(base.map((v) => v.size))]
  const order = ['S', 'M', 'L', 'XL', 'XXL', 'XXXL']
  return order.filter((s) => unique.includes(s))
})

// Check if a size is in stock for the selected color
function isSizeInStock(size: string) {
  const match = props.variants.find(
    (v) => v.size === size && (props.selectedColor ? v.color === props.selectedColor : true) && v.stock > 0
  )
  return !!match
}

// The resolved variant for the current selection
const resolvedVariant = computed(() =>
  props.variants.find(
    (v) => v.color === props.selectedColor && v.size === props.selectedSize && v.stock > 0
  ) ?? null
)

defineExpose({ resolvedVariant })
</script>

<template>
  <div class="space-y-5">
    <!-- Color selection -->
    <div>
      <div class="flex items-center justify-between mb-2">
        <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-on-surface)]">
          Color
        </p>
        <p v-if="selectedColor" class="text-[length:var(--text-micro)] text-[color:var(--color-border-strong)]">
          {{ selectedColor }}
        </p>
      </div>
      <div class="flex gap-3 flex-wrap">
        <ColorSwatch
          v-for="color in colors"
          :key="color"
          :color="COLOR_BG[color] ?? color"
          :label="color"
          :selected="color === selectedColor"
          @click="emit('update:selectedColor', color)"
        />
      </div>
    </div>

    <!-- Size selection -->
    <div>
      <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-on-surface)] mb-2">
        Size
      </p>
      <div class="flex gap-2 flex-wrap">
        <SizeButton
          v-for="size in sizes"
          :key="size"
          :size="size"
          :selected="size === selectedSize"
          :available="isSizeInStock(size)"
          @select="emit('update:selectedSize', size)"
        />
      </div>
    </div>

    <!-- Stock warning for resolved variant -->
    <p
      v-if="resolvedVariant && resolvedVariant.stock <= 10"
      class="text-[length:var(--text-micro)] text-[color:var(--color-amber-accent)] tracking-[var(--tracking-label)] uppercase"
    >
      Only {{ resolvedVariant.stock }} left
    </p>
  </div>
</template>
