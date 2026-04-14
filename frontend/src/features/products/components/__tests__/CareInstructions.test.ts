import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import CareInstructions from '../CareInstructions.vue'

const CARE_DATA = {
  wash: 'Dry clean solamente',
  iron: 'Temperatura baja, vapor',
  store: 'Colgar, lejos de luz directa',
  material: '100% lana italiana 16 mic',
}

describe('CareInstructions', () => {
  it('renders 4 care items', () => {
    const wrapper = mount(CareInstructions, { props: { care: CARE_DATA, lineName: 'Polo Atelier' } })
    expect(wrapper.findAll('[data-care-item]')).toHaveLength(4)
  })

  it('displays the material', () => {
    const wrapper = mount(CareInstructions, { props: { care: CARE_DATA, lineName: 'Polo Atelier' } })
    expect(wrapper.text()).toContain('100% lana italiana 16 mic')
  })

  it('displays the line name in the header', () => {
    const wrapper = mount(CareInstructions, { props: { care: CARE_DATA, lineName: 'Polo Atelier' } })
    expect(wrapper.text()).toContain('Polo Atelier')
  })
})
