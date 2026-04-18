<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCartStore } from '@features/cart/store'
import OrderConfirmCard from './OrderConfirmCard.vue'
import SeoHead from '@shared/components/SeoHead.vue'

const route = useRoute()
const cart = useCartStore()
const orderId = (route.query.order as string) ?? ''

onMounted(() => {
  cart.clear()
})
</script>

<template>
  <SeoHead
    title="Order Confirmed — Vantier"
    description="Your order has been confirmed."
    :robots="{ index: false, follow: false }"
  />
  <OrderConfirmCard :order-id="orderId" />
</template>
