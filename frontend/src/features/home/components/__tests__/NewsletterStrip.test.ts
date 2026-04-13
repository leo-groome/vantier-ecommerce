import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import NewsletterStrip from '../NewsletterStrip.vue'

describe('NewsletterStrip', () => {
  it('renders an anchor tag (not a form)', () => {
    const wrapper = mount(NewsletterStrip)
    expect(wrapper.find('form').exists()).toBe(false)
    expect(wrapper.find('a[data-newsletter-cta]').exists()).toBe(true)
  })

  it('opens in a new tab', () => {
    const wrapper = mount(NewsletterStrip)
    const link = wrapper.find('a[data-newsletter-cta]')
    expect(link.attributes('target')).toBe('_blank')
    expect(link.attributes('rel')).toContain('noopener')
  })
})
