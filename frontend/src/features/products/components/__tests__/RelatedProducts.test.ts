import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import RelatedProducts from '../RelatedProducts.vue'
import { createRouter, createMemoryHistory } from 'vue-router'

const router = createRouter({ history: createMemoryHistory(), routes: [{ path: '/:pathMatch(.*)*', component: { template: '<div/>' } }] })

const LINES = [
  { line: 'Signature', href: '/shop?line=signature' },
  { line: 'Essential', href: '/shop?line=essential' },
]

describe('RelatedProducts', () => {
  it('renders the related lines passed as props', async () => {
    const wrapper = mount(RelatedProducts, {
      props: { relatedLines: LINES },
      global: { plugins: [router] },
    })
    await router.isReady()
    expect(wrapper.findAll('[data-related-card]')).toHaveLength(2)
  })

  it('renders a shop-all editorial tile', async () => {
    const wrapper = mount(RelatedProducts, {
      props: { relatedLines: LINES },
      global: { plugins: [router] },
    })
    await router.isReady()
    expect(wrapper.find('[data-shop-all]').exists()).toBe(true)
  })
})
