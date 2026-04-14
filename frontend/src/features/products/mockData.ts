import type { Product } from './types'

// Color → CSS background mapping — palette: black / white / gold only
export const COLOR_BG: Record<string, string> = {
  'Ivory':      'oklch(97% 0.003 90)',   // white
  'Obsidian':   'oklch(8%  0.005 250)',  // black
  'Midnight':   'oklch(8%  0.005 250)',  // black
  'Warm Beige': 'oklch(97% 0.003 90)',   // white
  'Charcoal':   'oklch(8%  0.005 250)',  // black
}

export const COLOR_TEXT: Record<string, string> = {
  'Ivory':      'oklch(8%  0.005 250)',  // black on white
  'Obsidian':   'oklch(97% 0.003 90)',   // white on black
  'Midnight':   'oklch(97% 0.003 90)',   // white on black
  'Warm Beige': 'oklch(8%  0.005 250)',  // black on white
  'Charcoal':   'oklch(97% 0.003 90)',   // white on black
}

export const MOCK_PRODUCTS: Product[] = [
  // ── Polo Atelier ──────────────────────────────────────────
  {
    id: 'pa-classic-ivory',
    name: 'Polo Atelier — Classic',
    line: 'Polo Atelier',
    style: 'Classic',
    priceUSD: 180,
    description: 'The cornerstone piece. Crafted from 100% Pima cotton with a structured collar and refined silhouette.',
    images: [
      { id: 'pa-ci-img1', url: '/images/Products/polo-atelier-beige-folded.jpg',    alt: 'Polo Atelier Classic — Ivory, folded', isPrimary: true  },
      { id: 'pa-ci-img2', url: '/images/Products/polo-atelier-jackets-stacked.jpg', alt: 'Polo Atelier — color range',            isPrimary: false },
    ],
    variants: [
      { id: 'pa-ci-s',  sku: 'PA-CL-IVY-S',  size: 'S',  color: 'Ivory',    stock: 12 },
      { id: 'pa-ci-m',  sku: 'PA-CL-IVY-M',  size: 'M',  color: 'Ivory',    stock: 8  },
      { id: 'pa-ci-l',  sku: 'PA-CL-IVY-L',  size: 'L',  color: 'Ivory',    stock: 3  },
      { id: 'pa-ci-xl', sku: 'PA-CL-IVY-XL', size: 'XL', color: 'Ivory',    stock: 6  },
    ],
  },
  {
    id: 'pa-classic-obsidian',
    name: 'Polo Atelier — Classic',
    line: 'Polo Atelier',
    style: 'Classic',
    priceUSD: 180,
    description: 'The cornerstone piece. Crafted from 100% Pima cotton with a structured collar and refined silhouette.',
    images: [
      { id: 'pa-co-img1', url: '/images/Products/polo-atelier-jackets-stacked.jpg', alt: 'Polo Atelier Classic — Obsidian', isPrimary: true  },
      { id: 'pa-co-img2', url: '/images/Products/polo-atelier-lifestyle.jpg',        alt: 'Polo Atelier lifestyle',          isPrimary: false },
    ],
    variants: [
      { id: 'pa-co-s',  sku: 'PA-CL-OBS-S',  size: 'S',  color: 'Obsidian', stock: 10 },
      { id: 'pa-co-m',  sku: 'PA-CL-OBS-M',  size: 'M',  color: 'Obsidian', stock: 6  },
      { id: 'pa-co-l',  sku: 'PA-CL-OBS-L',  size: 'L',  color: 'Obsidian', stock: 0  },
      { id: 'pa-co-xl', sku: 'PA-CL-OBS-XL', size: 'XL', color: 'Obsidian', stock: 4  },
    ],
  },
  {
    id: 'pa-design-obsidian',
    name: 'Polo Atelier — Design',
    line: 'Polo Atelier',
    style: 'Design',
    priceUSD: 195,
    description: 'Architectural collar construction. Contrast stitching detail. A study in controlled asymmetry.',
    images: [
      { id: 'pa-do-img1', url: '/images/Products/polo-atelier-lifestyle.jpg',        alt: 'Polo Atelier Design — lifestyle',   isPrimary: true  },
      { id: 'pa-do-img2', url: '/images/Products/polo-atelier-jackets-stacked.jpg',  alt: 'Polo Atelier — color range',        isPrimary: false },
    ],
    variants: [
      { id: 'pa-do-m',  sku: 'PA-DS-OBS-M',  size: 'M',  color: 'Obsidian', stock: 9 },
      { id: 'pa-do-l',  sku: 'PA-DS-OBS-L',  size: 'L',  color: 'Obsidian', stock: 3 },
      { id: 'pa-do-xl', sku: 'PA-DS-OBS-XL', size: 'XL', color: 'Obsidian', stock: 1 },
    ],
  },
  {
    id: 'pa-design-midnight',
    name: 'Polo Atelier — Design',
    line: 'Polo Atelier',
    style: 'Design',
    priceUSD: 195,
    description: 'Architectural collar construction. Contrast stitching detail. A study in controlled asymmetry.',
    images: [
      { id: 'pa-dm-img1', url: '/images/Products/polo-atelier-jackets-stacked.jpg', alt: 'Polo Atelier Design — Midnight', isPrimary: true },
    ],
    variants: [
      { id: 'pa-dm-m', sku: 'PA-DS-MID-M', size: 'M', color: 'Midnight', stock: 7 },
      { id: 'pa-dm-l', sku: 'PA-DS-MID-L', size: 'L', color: 'Midnight', stock: 5 },
    ],
  },
  // ── Signature ─────────────────────────────────────────────
  {
    id: 'sig-design-midnight',
    name: 'Signature Shirt',
    line: 'Signature',
    style: 'Design',
    priceUSD: 220,
    description: 'Impeccably tailored. Woven from premium long-staple Egyptian cotton for a drape that commands presence.',
    images: [
      { id: 'sig-img1', url: '/images/Products/signature-lifestyle.jpg',      alt: 'Signature Shirt — lifestyle',    isPrimary: true  },
      { id: 'sig-img2', url: '/images/Products/signature-shirts-stacked.jpg', alt: 'Signature — color range',        isPrimary: false },
    ],
    variants: [
      { id: 'sig-m',  sku: 'SIG-DS-MID-M',  size: 'M',  color: 'Midnight', stock: 7 },
      { id: 'sig-l',  sku: 'SIG-DS-MID-L',  size: 'L',  color: 'Midnight', stock: 4 },
      { id: 'sig-xl', sku: 'SIG-DS-MID-XL', size: 'XL', color: 'Midnight', stock: 2 },
    ],
  },
  {
    id: 'sig-classic-ivory',
    name: 'Signature Shirt — Classic',
    line: 'Signature',
    style: 'Classic',
    priceUSD: 205,
    description: 'The everyday formal. Crisp cotton poplin with a refined spread collar. Effortlessly pristine.',
    images: [
      { id: 'sigc-img1', url: '/images/Products/signature-blazer-street.jpg',    alt: 'Signature Classic — street editorial', isPrimary: true  },
      { id: 'sigc-img2', url: '/images/Products/signature-blazer-lifestyle.jpg', alt: 'Signature Classic — lifestyle',        isPrimary: false },
      { id: 'sigc-img3', url: '/images/Products/signature-shirts-stacked.jpg',   alt: 'Signature — color range',              isPrimary: false },
    ],
    variants: [
      { id: 'sigc-s', sku: 'SIG-CL-IVY-S', size: 'S', color: 'Ivory', stock: 15 },
      { id: 'sigc-m', sku: 'SIG-CL-IVY-M', size: 'M', color: 'Ivory', stock: 12 },
      { id: 'sigc-l', sku: 'SIG-CL-IVY-L', size: 'L', color: 'Ivory', stock: 8  },
    ],
  },
  // ── Essential ─────────────────────────────────────────────
  {
    id: 'ess-classic-ivory',
    name: 'Essential Tee',
    line: 'Essential',
    style: 'Classic',
    priceUSD: 95,
    description: 'The everyday foundation. Supima cotton, relaxed silhouette. Understated by design.',
    images: [
      { id: 'ess-ci-img1', url: '/images/Products/essential-white.jpg', alt: 'Essential Tee — Ivory', isPrimary: true },
    ],
    variants: [
      { id: 'ess-ci-s',  sku: 'ESS-CL-IVY-S',  size: 'S',  color: 'Ivory', stock: 20 },
      { id: 'ess-ci-m',  sku: 'ESS-CL-IVY-M',  size: 'M',  color: 'Ivory', stock: 15 },
      { id: 'ess-ci-l',  sku: 'ESS-CL-IVY-L',  size: 'L',  color: 'Ivory', stock: 10 },
      { id: 'ess-ci-xl', sku: 'ESS-CL-IVY-XL', size: 'XL', color: 'Ivory', stock: 5  },
    ],
  },
  {
    id: 'ess-classic-warmbeige',
    name: 'Essential Tee',
    line: 'Essential',
    style: 'Classic',
    priceUSD: 95,
    description: 'The everyday foundation. Supima cotton, relaxed silhouette. Understated by design.',
    images: [
      { id: 'ess-wb-img1', url: '/images/Products/essential-white.jpg',    alt: 'Essential Tee — Warm Beige',   isPrimary: true  },
      { id: 'ess-wb-img2', url: '/images/Products/essential-blue-tees.jpg', alt: 'Essential Tee — color range', isPrimary: false },
    ],
    variants: [
      { id: 'ess-wb-s', sku: 'ESS-CL-WB-S', size: 'S', color: 'Warm Beige', stock: 8 },
      { id: 'ess-wb-m', sku: 'ESS-CL-WB-M', size: 'M', color: 'Warm Beige', stock: 4 },
      { id: 'ess-wb-l', sku: 'ESS-CL-WB-L', size: 'L', color: 'Warm Beige', stock: 2 },
    ],
  },
  {
    id: 'ess-classic-obsidian',
    name: 'Essential Tee',
    line: 'Essential',
    style: 'Classic',
    priceUSD: 95,
    description: 'The everyday foundation. Supima cotton, relaxed silhouette. Understated by design.',
    images: [
      { id: 'ess-ob-img1', url: '/images/Products/essential-blue-tees.jpg',   alt: 'Essential Tee — Obsidian',    isPrimary: true  },
      { id: 'ess-ob-img2', url: '/images/Products/essential-blue-detail.jpg',  alt: 'Essential Tee — logo detail', isPrimary: false },
    ],
    variants: [
      { id: 'ess-ob-s', sku: 'ESS-CL-OBS-S', size: 'S', color: 'Obsidian', stock: 18 },
      { id: 'ess-ob-m', sku: 'ESS-CL-OBS-M', size: 'M', color: 'Obsidian', stock: 14 },
      { id: 'ess-ob-l', sku: 'ESS-CL-OBS-L', size: 'L', color: 'Obsidian', stock: 9  },
    ],
  },
]
