import { describe, it, expect } from 'vitest'
import { formatUSD, formatDate, formatSize } from '@shared/utils/formatters'

describe('formatUSD', () => {
  it('formats whole dollars', () => {
    expect(formatUSD(120)).toBe('$120.00')
  })
  it('formats cents', () => {
    expect(formatUSD(99.9)).toBe('$99.90')
  })
  it('formats zero', () => {
    expect(formatUSD(0)).toBe('$0.00')
  })
})

describe('formatDate', () => {
  it('formats ISO string to readable date', () => {
    expect(formatDate('2026-04-10T00:00:00Z')).toBe('Apr 10, 2026')
  })
})

describe('formatSize', () => {
  it('returns size as uppercase string', () => {
    expect(formatSize('s')).toBe('S')
    expect(formatSize('XL')).toBe('XL')
  })
})
