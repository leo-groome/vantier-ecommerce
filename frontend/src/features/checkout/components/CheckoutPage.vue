<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCheckoutStore } from '../store'
import type { ShippingRate } from '../types'
import CheckoutStepper from './CheckoutStepper.vue'
import GuestEmailInput from './GuestEmailInput.vue'
import AddressForm from './AddressForm.vue'
import type { AddressData } from './AddressForm.vue'
import ShippingMethodSelect from './ShippingMethodSelect.vue'
import StripePaymentForm from './StripePaymentForm.vue'
import OrderSummaryPanel from './OrderSummaryPanel.vue'
import SeoHead from '@shared/components/SeoHead.vue'
import DiscountCodeInput from '@features/cart/components/DiscountCodeInput.vue'

const checkout = useCheckoutStore()
const router = useRouter()

const guestEmail = ref('')
const addressData = ref<AddressData | null>(null)

function onAddressSubmit(data: AddressData) {
  addressData.value = data
  checkout.step = 'shipping'
}

function onShippingSelect(rate: ShippingRate) {
  checkout.shippingRate = rate
}

function onShippingContinue() {
  if (checkout.shippingRate) checkout.step = 'payment'
}

function onPaymentSuccess(paymentIntentId: string) {
  checkout.paymentIntentId = paymentIntentId
  // Generate a placeholder order ID — real ID comes from backend response
  router.push(`/order-confirm/${paymentIntentId.slice(-8).toUpperCase()}`)
}

function onPaymentError(msg: string) {
  console.error('Payment error:', msg)
}
</script>

<template>
  <SeoHead
    title="Checkout — Vantier"
    description="Complete your order"
    :robots="{ index: false, follow: false }"
  />

  <div class="max-w-[var(--container-max)] mx-auto px-[var(--spacing-container)] py-12">
    <CheckoutStepper :current-step="checkout.step" />

    <div class="grid grid-cols-1 lg:grid-cols-[1fr_360px] gap-12">
      <!-- Left: form steps -->
      <div>
        <!-- Step 1: Address -->
        <template v-if="checkout.step === 'address'">
          <h2 class="text-[length:var(--text-title)] font-semibold mb-6 text-[color:var(--color-on-surface)]">
            Contact & Address
          </h2>
          <div class="space-y-4">
            <GuestEmailInput v-model="guestEmail" />
            <AddressForm @submit="onAddressSubmit" />
          </div>
        </template>

        <!-- Step 2: Shipping -->
        <template v-else-if="checkout.step === 'shipping'">
          <h2 class="text-[length:var(--text-title)] font-semibold mb-6 text-[color:var(--color-on-surface)]">
            Shipping Method
          </h2>
          <ShippingMethodSelect
            :zip="addressData?.zip ?? ''"
            @select="onShippingSelect"
          />
          <button
            class="mt-6 w-full py-4 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-[length:var(--text-small)] tracking-[var(--tracking-label)] uppercase hover:opacity-80 disabled:opacity-40 transition-opacity duration-[var(--duration-normal)]"
            :disabled="!checkout.shippingRate"
            @click="onShippingContinue"
          >
            Continue to Payment
          </button>
        </template>

        <!-- Step 3: Payment -->
        <template v-else-if="checkout.step === 'payment'">
          <h2 class="text-[length:var(--text-title)] font-semibold mb-6 text-[color:var(--color-on-surface)]">
            Payment
          </h2>
          <div class="mb-8">
            <DiscountCodeInput />
          </div>
          <StripePaymentForm
            @success="onPaymentSuccess"
            @error="onPaymentError"
          />
        </template>
      </div>

      <!-- Right: order summary -->
      <OrderSummaryPanel :shipping-rate="checkout.shippingRate" />
    </div>
  </div>
</template>
