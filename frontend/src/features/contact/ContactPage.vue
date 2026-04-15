<script setup lang="ts">
import { ref } from 'vue'
import SeoHead from '@shared/components/SeoHead.vue'
import SectionLabel from '@shared/components/SectionLabel.vue'

const form = ref({ name: '', email: '', subject: 'general', message: '' })
const submitted = ref(false)
const submitting = ref(false)

async function submit() {
  if (!form.value.name || !form.value.email || !form.value.message) return
  submitting.value = true
  await new Promise(r => setTimeout(r, 800))
  submitted.value = true
  submitting.value = false
}
</script>

<template>
  <SeoHead
    title="Contact — Vantier"
    description="Get in touch with Vantier. Exchange policy, shipping inquiries, and general questions."
    canonical="https://vantierluxuryla.com/contact"
  />

  <div class="max-w-[var(--container-max)] mx-auto px-[var(--spacing-container)] py-16">
    <div class="mb-12">
      <SectionLabel text="Get In Touch" />
      <h1 class="mt-3 text-[length:var(--text-headline)] font-light uppercase tracking-[var(--tracking-headline)]">
        Contact Us
      </h1>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-16">
      <!-- Info -->
      <div class="space-y-10">
        <div
          v-for="info in infoItems"
          :key="info.title"
          class="space-y-2"
        >
          <div class="flex items-center gap-3 mb-3">
            <div class="w-6 h-px bg-[color:var(--color-amber-accent)]" />
            <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] font-medium">{{ info.title }}</p>
          </div>
          <p class="text-[length:var(--text-small)] leading-relaxed opacity-70">{{ info.body }}</p>
          <p v-if="info.sub" class="text-[length:var(--text-micro)] opacity-50">{{ info.sub }}</p>
        </div>
      </div>

      <!-- Form -->
      <div>
        <div v-if="submitted" class="flex flex-col items-start gap-4 py-12">
          <div class="w-10 h-10 rounded-full bg-[color:var(--color-obsidian)] flex items-center justify-center">
            <svg class="w-5 h-5 text-[color:var(--color-ivory)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
          </div>
          <p class="text-[length:var(--text-title)] font-light uppercase tracking-[var(--tracking-headline)]">Message Sent</p>
          <p class="text-[length:var(--text-small)] opacity-60">We'll get back to you within 24 hours.</p>
          <button
            class="mt-4 text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-50 hover:opacity-100 transition-opacity"
            @click="submitted = false; form = { name: '', email: '', subject: 'general', message: '' }"
          >Send another message</button>
        </div>

        <form v-else class="space-y-5" @submit.prevent="submit">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-50 mb-2">Name</label>
              <input
                v-model="form.name"
                type="text"
                required
                placeholder="Your name"
                class="w-full border border-[color:var(--color-border)] px-4 py-3 text-[length:var(--text-small)] bg-transparent focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)]"
              />
            </div>
            <div>
              <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-50 mb-2">Email</label>
              <input
                v-model="form.email"
                type="email"
                required
                placeholder="your@email.com"
                class="w-full border border-[color:var(--color-border)] px-4 py-3 text-[length:var(--text-small)] bg-transparent focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)]"
              />
            </div>
          </div>

          <div>
            <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-50 mb-2">Subject</label>
            <select
              v-model="form.subject"
              class="w-full border border-[color:var(--color-border)] px-4 py-3 text-[length:var(--text-small)] bg-[color:var(--color-surface)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)]"
            >
              <option value="general">General Inquiry</option>
              <option value="exchange">Exchange / Return</option>
              <option value="shipping">Shipping Question</option>
              <option value="order">Order Issue</option>
              <option value="wholesale">Wholesale</option>
            </select>
          </div>

          <div>
            <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-50 mb-2">Message</label>
            <textarea
              v-model="form.message"
              required
              rows="6"
              placeholder="How can we help you?"
              class="w-full border border-[color:var(--color-border)] px-4 py-3 text-[length:var(--text-small)] bg-transparent focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)] resize-none"
            />
          </div>

          <button
            type="submit"
            :disabled="submitting"
            class="w-full py-4 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-[length:var(--text-small)] uppercase tracking-[var(--tracking-label)] hover:opacity-80 disabled:opacity-50 transition-opacity duration-[var(--duration-normal)] flex items-center justify-center gap-3"
          >
            <span v-if="submitting" class="w-4 h-4 border-2 border-[color:var(--color-ivory)] border-t-transparent rounded-full animate-spin" />
            Send Message
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
const infoItems = [
  {
    title: 'Exchange Policy',
    body: 'We accept exchanges within 14 days of delivery. Items must be unworn, unwashed, and in original packaging.',
    sub: 'No cash refunds — exchange or store credit only.',
  },
  {
    title: 'Shipping',
    body: 'Free shipping on orders of 5+ items. Standard delivery 5–7 business days. Express options available at checkout.',
    sub: 'We ship to México, USA, and select international destinations.',
  },
  {
    title: 'Response Time',
    body: 'Our team responds to all inquiries within 24 hours, Monday through Friday.',
    sub: 'For urgent order issues, reference your order number.',
  },
  {
    title: 'Location',
    body: 'Los Angeles, California — México City operations.',
    sub: 'vantierluxuryla.com',
  },
]
</script>
