<script setup lang="ts">
import { useRoute } from 'vue-router'
import OrderConfirmCard from './OrderConfirmCard.vue'
import SeoHead from '@shared/components/SeoHead.vue'

const route = useRoute()
const orderId = route.params.orderId as string
</script>

<template>
  <SeoHead
    :title="`Order #${orderId} Confirmed — Vantier`"
    description="Your order has been confirmed."
    :robots="{ index: false, follow: false }"
  />
  <OrderConfirmCard :order-id="orderId" />
</template>
