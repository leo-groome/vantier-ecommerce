<script setup lang="ts">
import HeroCarousel from '../components/HeroCarousel.vue'
import ProductLineGrid from '../components/ProductLineGrid.vue'
import FeaturedProducts from '../components/FeaturedProducts.vue'
import BrandStatement from '../components/BrandStatement.vue'
import ElProceso from '../components/ElProceso.vue'
import NewsletterStrip from '../components/NewsletterStrip.vue'
import SeoHead from '@shared/components/SeoHead.vue'
</script>
<template>
  <SeoHead
    title="Vantier — Silent Luxury Menswear | Los Angeles"
    description="Vantier crafts elevated menswear for the discerning modern man. Polo Atelier jackets, Signature shirts, and Essential tees. Free shipping on 5+ items."
    canonical="https://vantierluxuryla.com/"
  />
  <HeroCarousel />
  <ProductLineGrid />
  <FeaturedProducts />
  <BrandStatement />
  <ElProceso />
  <NewsletterStrip />
</template>
