<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const emit = defineEmits<{ (e: 'success', paymentIntentId: string): void; (e: 'error', msg: string): void }>()

const stripeReady = ref(false)
const submitting = ref(false)
const errorMsg = ref('')

// Stripe Elements will mount here
const cardEl = ref<HTMLDivElement | null>(null)

let stripe: unknown = null
let elements: unknown = null
let card: unknown = null

onMounted(async () => {
  // Lazy-load Stripe.js — only executed on the payment step
  const { loadStripe } = await import('@stripe/stripe-js')
  const stripeKey = import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY ?? ''
  if (!stripeKey) {
    errorMsg.value = 'Payment not configured (missing VITE_STRIPE_PUBLISHABLE_KEY)'
    return
  }
  stripe = await loadStripe(stripeKey)
  if (!stripe) return

  // @ts-expect-error - stripe is typed as Stripe | null from the library
  elements = stripe.elements()
  // @ts-expect-error
  card = elements.create('card', {
    style: {
      base: {
        fontFamily: 'Inter, sans-serif',
        fontSize: '14px',
        color: 'oklch(8% 0.005 250)',
        '::placeholder': { color: 'oklch(70% 0.012 80)' },
      },
      invalid: { color: '#dc2626' },
    },
  })
  if (cardEl.value) {
    // @ts-expect-error
    card.mount(cardEl.value)
  }
  stripeReady.value = true
})

onUnmounted(() => {
  // @ts-expect-error
  card?.unmount?.()
})

async function submit() {
  if (!stripe || !card || submitting.value) return
  submitting.value = true
  errorMsg.value = ''
  try {
    // TODO: fetch clientSecret from backend /api/orders/payment-intent
    const clientSecret = import.meta.env.VITE_STRIPE_CLIENT_SECRET_PLACEHOLDER ?? ''
    // @ts-expect-error
    const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
      // @ts-expect-error
      payment_method: { card },
    })
    if (error) {
      errorMsg.value = error.message ?? 'Payment failed'
    } else if (paymentIntent?.status === 'succeeded') {
      emit('success', paymentIntent.id)
    }
  } catch (e) {
    errorMsg.value = 'An unexpected error occurred'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="space-y-4">
    <div
      ref="cardEl"
      class="border border-[color:var(--color-border)] p-3.5 min-h-[42px]"
      :class="{ 'opacity-50': !stripeReady }"
    />
    <p v-if="!stripeReady && !errorMsg" class="text-[length:var(--text-micro)] text-[color:var(--color-border-strong)]">
      Loading payment form…
    </p>
    <p v-if="errorMsg" class="text-[length:var(--text-micro)] text-red-600">{{ errorMsg }}</p>

    <button
      :disabled="!stripeReady || submitting"
      class="w-full py-4 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-[length:var(--text-small)] tracking-[var(--tracking-label)] uppercase hover:opacity-80 disabled:opacity-40 transition-opacity duration-[var(--duration-normal)] flex items-center justify-center gap-3"
      @click="submit"
    >
      <span v-if="submitting" class="w-4 h-4 border-2 border-[color:var(--color-ivory)] border-t-transparent rounded-full animate-spin" />
      <span>{{ submitting ? 'Processing…' : 'Place Order' }}</span>
    </button>

    <p class="text-center text-[length:var(--text-micro)] text-[color:var(--color-border-strong)]">
      Secured by Stripe · SSL encrypted
    </p>
  </div>
</template>
