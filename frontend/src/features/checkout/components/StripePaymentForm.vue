<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { loadStripe } from '@stripe/stripe-js'
import type { Stripe, StripeElements } from '@stripe/stripe-js'

const props = defineProps<{
  clientSecret: string
  orderId: string
}>()

const emit = defineEmits<{
  (e: 'success'): void
  (e: 'error', message: string): void
}>()

const containerRef = ref<HTMLDivElement | null>(null)
const stripe = ref<Stripe | null>(null)
const elements = ref<StripeElements | null>(null)
const loading = ref(true)
const submitting = ref(false)
const errorMessage = ref('')

onMounted(async () => {
  const pk = import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY
  if (!pk) {
    errorMessage.value = 'Payment service not configured.'
    loading.value = false
    return
  }

  stripe.value = await loadStripe(pk)
  if (!stripe.value) {
    errorMessage.value = 'Could not load payment service.'
    loading.value = false
    return
  }

  elements.value = stripe.value.elements({
    clientSecret: props.clientSecret,
    appearance: {
      theme: 'flat',
      variables: {
        colorPrimary: '#1a1a1a',
        colorBackground: '#fafaf8',
        colorText: '#1a1a1a',
        colorDanger: '#c0392b',
        fontFamily: 'inherit',
        borderRadius: '0px',
        spacingUnit: '4px',
      },
    },
  })

  const paymentElement = elements.value.create('payment')
  paymentElement.on('ready', () => { loading.value = false })
  paymentElement.on('loaderror', (e) => {
    console.error('[Stripe] loaderror:', e)
    errorMessage.value = `Stripe load error: ${(e as any)?.error?.message ?? 'unknown'}`
    loading.value = false
  })
  paymentElement.mount(containerRef.value!)

  // Fallback: if ready never fires after 8s, show error
  setTimeout(() => {
    if (loading.value) {
      console.error('[Stripe] Payment Element never fired ready — check publishable key vs client_secret mismatch')
      errorMessage.value = 'Payment form failed to load. Check browser console for details.'
      loading.value = false
    }
  }, 8000)
})

onBeforeUnmount(() => {
  elements.value?.getElement('payment')?.destroy()
})

async function handleSubmit() {
  if (!stripe.value || !elements.value || submitting.value) return
  submitting.value = true
  errorMessage.value = ''

  const { error } = await stripe.value.confirmPayment({
    elements: elements.value,
    confirmParams: {
      return_url: `${window.location.origin}/checkout/success?order_id=${props.orderId}`,
    },
    redirect: 'if_required',
  })

  if (error) {
    errorMessage.value = error.message ?? 'Payment failed. Please try again.'
    submitting.value = false
    emit('error', errorMessage.value)
  } else {
    emit('success')
  }
}
</script>

<template>
  <div class="space-y-6">
    <!-- Payment Element mount point -->
    <div
      ref="containerRef"
      class="min-h-[120px] border border-[color:var(--color-border)] p-4"
      :class="{ 'opacity-0': loading }"
    />

    <!-- Skeleton while loading -->
    <div v-if="loading" class="space-y-3 -mt-[calc(120px+1.5rem)]">
      <div class="h-10 bg-[color:var(--color-warm-beige)] animate-pulse" />
      <div class="h-10 bg-[color:var(--color-warm-beige)] animate-pulse" />
    </div>

    <!-- Error -->
    <p v-if="errorMessage" class="text-[length:var(--text-micro)] text-red-600">
      {{ errorMessage }}
    </p>

    <!-- Submit -->
    <button
      :disabled="loading || submitting"
      class="w-full py-4 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-[length:var(--text-small)] tracking-[var(--tracking-label)] uppercase hover:opacity-80 disabled:opacity-40 transition-opacity duration-[var(--duration-normal)] flex items-center justify-center gap-3"
      @click="handleSubmit"
    >
      <span
        v-if="submitting"
        class="w-4 h-4 border-2 border-[color:var(--color-ivory)] border-t-transparent rounded-full animate-spin"
      />
      <span>{{ submitting ? 'Processing…' : 'Pay now' }}</span>
    </button>

    <p class="text-center text-[length:var(--text-micro)] text-[color:var(--color-border-strong)]">
      Secured by Stripe · SSL encrypted
    </p>
  </div>
</template>
