import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import ElProceso from '../ElProceso.vue'

describe('ElProceso', () => {
  it('renders 3 steps', () => {
    const wrapper = mount(ElProceso)
    expect(wrapper.findAll('[data-step]')).toHaveLength(3)
  })

  it('renders step numbers 01, 02, 03', () => {
    const wrapper = mount(ElProceso)
    const numbers = wrapper.findAll('[data-step-number]').map(el => el.text())
    expect(numbers).toEqual(['01', '02', '03'])
  })

  it('renders step titles Diseño, Confección, Entrega', () => {
    const wrapper = mount(ElProceso)
    const titles = wrapper.findAll('[data-step-title]').map(el => el.text())
    expect(titles).toEqual(['Diseño', 'Confección', 'Entrega'])
  })
})
