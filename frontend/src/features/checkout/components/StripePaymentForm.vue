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

const demoMode = ref(false)

onMounted(async () => {
  // Lazy-load Stripe.js — only executed on the payment step
  const stripeKey = import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY ?? ''
  if (!stripeKey) {
    // No Stripe key — run in demo mode with a simulated payment
    demoMode.value = true
    stripeReady.value = true
    return
  }
  const { loadStripe } = await import('@stripe/stripe-js')
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
  if (submitting.value) return
  submitting.value = true
  errorMsg.value = ''
  try {
    if (demoMode.value) {
      // Simulate payment processing
      await new Promise(r => setTimeout(r, 1500))
      emit('success', `pi_demo_${Date.now()}`)
      return
    }
    if (!stripe || !card) return
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
    <!-- Demo mode banner -->
    <div v-if="demoMode" class="border border-amber-200 bg-amber-50 rounded-[var(--radius-md)] px-4 py-3 flex items-start gap-3">
      <svg class="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <div>
        <p class="text-xs font-medium text-amber-800 uppercase tracking-wider">Demo Mode</p>
        <p class="text-xs text-amber-700 mt-0.5">No Stripe key configured. Clicking "Place Order" simulates a successful payment.</p>
      </div>
    </div>

    <!-- Demo card fields (visual only) -->
    <div v-if="demoMode" class="space-y-3">
      <div class="border border-[color:var(--color-border)] p-3.5 bg-[color:var(--color-warm-beige)] rounded-[var(--radius-sm)]">
        <p class="text-[length:var(--text-micro)] text-[color:var(--color-border-strong)] mb-1 uppercase tracking-wider">Card number</p>
        <p class="text-[length:var(--text-small)] text-[color:var(--color-border-strong)] font-mono">4242 4242 4242 4242</p>
      </div>
      <div class="grid grid-cols-2 gap-3">
        <div class="border border-[color:var(--color-border)] p-3.5 bg-[color:var(--color-warm-beige)] rounded-[var(--radius-sm)]">
          <p class="text-[length:var(--text-micro)] text-[color:var(--color-border-strong)] mb-1 uppercase tracking-wider">Expiry</p>
          <p class="text-[length:var(--text-small)] text-[color:var(--color-border-strong)] font-mono">12 / 29</p>
        </div>
        <div class="border border-[color:var(--color-border)] p-3.5 bg-[color:var(--color-warm-beige)] rounded-[var(--radius-sm)]">
          <p class="text-[length:var(--text-micro)] text-[color:var(--color-border-strong)] mb-1 uppercase tracking-wider">CVC</p>
          <p class="text-[length:var(--text-small)] text-[color:var(--color-border-strong)] font-mono">•••</p>
        </div>
      </div>
    </div>

    <!-- Real Stripe Card Element -->
    <div
      v-else
      ref="cardEl"
      class="border border-[color:var(--color-border)] p-3.5 min-h-[42px]"
      :class="{ 'opacity-50': !stripeReady }"
    />
    <p v-if="!stripeReady && !demoMode && !errorMsg" class="text-[length:var(--text-micro)] text-[color:var(--color-border-strong)]">
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
