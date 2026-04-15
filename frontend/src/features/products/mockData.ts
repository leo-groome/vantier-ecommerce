import type { Product } from './types'

// ─── Real Vantier color palette ───────────────────────────────────────────────
export const COLOR_BG: Record<string, string> = {
  // Signature
  'Azul Vantier':    '#869AEB',
  'Beige Verano':    '#E8E6D6',
  'Naranja Vantier': '#F2955E',
  'Blanca':          '#FFFFFF',
  'Negra':           '#000000',
  // Polo Atelier
  'Beige Atelier':   '#C9BFA8',
  'Azul Navy':       '#202646',
  // Essential
  'Azul Essential':  '#2D3FA6',
}

export const COLOR_TEXT: Record<string, string> = {
  'Azul Vantier':    '#FFFFFF',
  'Beige Verano':    '#000000',
  'Naranja Vantier': '#FFFFFF',
  'Blanca':          '#000000',
  'Negra':           '#FFFFFF',
  'Beige Atelier':   '#000000',
  'Azul Navy':       '#FFFFFF',
  'Azul Essential':  '#FFFFFF',
}

export const MOCK_PRODUCTS: Product[] = [
  // ── Polo Atelier ──────────────────────────────────────────────────────────
  {
    id: 'pa-classic-beige',
    name: 'Polo Atelier — Classic',
    line: 'Polo Atelier',
    style: 'Classic',
    priceUSD: 180,
    description: 'The cornerstone piece. Crafted from 100% Pima cotton with a structured collar and refined silhouette.',
    images: [
      { id: 'pa-cb-img1', url: '/images/Products/polo-atelier-beige-folded.jpg',    alt: 'Polo Atelier — Beige Atelier', isPrimary: true  },
      { id: 'pa-cb-img2', url: '/images/Products/polo-atelier-jackets-stacked.jpg', alt: 'Polo Atelier — color range',   isPrimary: false },
    ],
    variants: [
      { id: 'pa-cb-s',  sku: 'PA-CL-BEI-S',  size: 'S',  color: 'Beige Atelier', stock: 12 },
      { id: 'pa-cb-m',  sku: 'PA-CL-BEI-M',  size: 'M',  color: 'Beige Atelier', stock: 8  },
      { id: 'pa-cb-l',  sku: 'PA-CL-BEI-L',  size: 'L',  color: 'Beige Atelier', stock: 3  },
      { id: 'pa-cb-xl', sku: 'PA-CL-BEI-XL', size: 'XL', color: 'Beige Atelier', stock: 6  },
    ],
  },
  {
    id: 'pa-classic-navy',
    name: 'Polo Atelier — Classic',
    line: 'Polo Atelier',
    style: 'Classic',
    priceUSD: 180,
    description: 'The cornerstone piece. Crafted from 100% Pima cotton with a structured collar and refined silhouette.',
    images: [
      { id: 'pa-cn-img1', url: '/images/Products/polo-atelier-jackets-stacked.jpg', alt: 'Polo Atelier — Azul Navy', isPrimary: true  },
      { id: 'pa-cn-img2', url: '/images/Products/polo-atelier-lifestyle.jpg',        alt: 'Polo Atelier lifestyle',  isPrimary: false },
    ],
    variants: [
      { id: 'pa-cn-s',  sku: 'PA-CL-NAV-S',  size: 'S',  color: 'Azul Navy', stock: 10 },
      { id: 'pa-cn-m',  sku: 'PA-CL-NAV-M',  size: 'M',  color: 'Azul Navy', stock: 6  },
      { id: 'pa-cn-l',  sku: 'PA-CL-NAV-L',  size: 'L',  color: 'Azul Navy', stock: 0  },
      { id: 'pa-cn-xl', sku: 'PA-CL-NAV-XL', size: 'XL', color: 'Azul Navy', stock: 4  },
    ],
  },
  {
    id: 'pa-classic-negra',
    name: 'Polo Atelier — Classic',
    line: 'Polo Atelier',
    style: 'Classic',
    priceUSD: 180,
    description: 'The cornerstone piece. Crafted from 100% Pima cotton with a structured collar and refined silhouette.',
    images: [
      { id: 'pa-co-img1', url: '/images/Products/polo-atelier-jackets-stacked.jpg', alt: 'Polo Atelier — Negra',   isPrimary: true  },
      { id: 'pa-co-img2', url: '/images/Products/polo-atelier-lifestyle.jpg',        alt: 'Polo Atelier lifestyle', isPrimary: false },
    ],
    variants: [
      { id: 'pa-co-s',  sku: 'PA-CL-NEG-S',  size: 'S',  color: 'Negra', stock: 9  },
      { id: 'pa-co-m',  sku: 'PA-CL-NEG-M',  size: 'M',  color: 'Negra', stock: 7  },
      { id: 'pa-co-l',  sku: 'PA-CL-NEG-L',  size: 'L',  color: 'Negra', stock: 3  },
      { id: 'pa-co-xl', sku: 'PA-CL-NEG-XL', size: 'XL', color: 'Negra', stock: 5  },
    ],
  },

  // ── Signature ─────────────────────────────────────────────────────────────
  {
    id: 'sig-azul-vantier',
    name: 'Signature Shirt',
    line: 'Signature',
    style: 'Design',
    priceUSD: 220,
    description: 'Impeccably tailored. Woven from premium long-staple Egyptian cotton for a drape that commands presence.',
    images: [
      { id: 'sig-az-img1', url: '/images/Products/signature-lifestyle.jpg',      alt: 'Signature — Azul Vantier', isPrimary: true  },
      { id: 'sig-az-img2', url: '/images/Products/signature-shirts-stacked.jpg', alt: 'Signature — color range',  isPrimary: false },
    ],
    variants: [
      { id: 'sig-az-s',  sku: 'SIG-AZ-S',  size: 'S',  color: 'Azul Vantier', stock: 8 },
      { id: 'sig-az-m',  sku: 'SIG-AZ-M',  size: 'M',  color: 'Azul Vantier', stock: 6 },
      { id: 'sig-az-l',  sku: 'SIG-AZ-L',  size: 'L',  color: 'Azul Vantier', stock: 4 },
      { id: 'sig-az-xl', sku: 'SIG-AZ-XL', size: 'XL', color: 'Azul Vantier', stock: 2 },
    ],
  },
  {
    id: 'sig-beige-verano',
    name: 'Signature Shirt',
    line: 'Signature',
    style: 'Classic',
    priceUSD: 205,
    description: 'The everyday formal. Crisp cotton poplin with a refined spread collar. Effortlessly pristine.',
    images: [
      { id: 'sig-be-img1', url: '/images/Products/signature-blazer-street.jpg',    alt: 'Signature — Beige Verano', isPrimary: true  },
      { id: 'sig-be-img2', url: '/images/Products/signature-blazer-lifestyle.jpg', alt: 'Signature — lifestyle',    isPrimary: false },
    ],
    variants: [
      { id: 'sig-be-s',  sku: 'SIG-BE-S',  size: 'S',  color: 'Beige Verano', stock: 10 },
      { id: 'sig-be-m',  sku: 'SIG-BE-M',  size: 'M',  color: 'Beige Verano', stock: 8  },
      { id: 'sig-be-l',  sku: 'SIG-BE-L',  size: 'L',  color: 'Beige Verano', stock: 5  },
    ],
  },
  {
    id: 'sig-naranja-vantier',
    name: 'Signature Shirt',
    line: 'Signature',
    style: 'Design',
    priceUSD: 220,
    description: 'Arquitectura de color. Una declaración de presencia sin esfuerzo en algodón egipcio de primera calidad.',
    images: [
      { id: 'sig-na-img1', url: '/images/Products/signature-lifestyle.jpg',      alt: 'Signature — Naranja Vantier', isPrimary: true  },
      { id: 'sig-na-img2', url: '/images/Products/signature-shirts-stacked.jpg', alt: 'Signature — color range',     isPrimary: false },
    ],
    variants: [
      { id: 'sig-na-s',  sku: 'SIG-NA-S',  size: 'S',  color: 'Naranja Vantier', stock: 6 },
      { id: 'sig-na-m',  sku: 'SIG-NA-M',  size: 'M',  color: 'Naranja Vantier', stock: 5 },
      { id: 'sig-na-l',  sku: 'SIG-NA-L',  size: 'L',  color: 'Naranja Vantier', stock: 3 },
    ],
  },
  {
    id: 'sig-blanca',
    name: 'Signature Shirt',
    line: 'Signature',
    style: 'Classic',
    priceUSD: 205,
    description: 'The everyday formal. Crisp cotton poplin with a refined spread collar. Effortlessly pristine.',
    images: [
      { id: 'sig-bl-img1', url: '/images/Products/signature-blazer-street.jpg', alt: 'Signature — Blanca', isPrimary: true },
    ],
    variants: [
      { id: 'sig-bl-s',  sku: 'SIG-BL-S',  size: 'S',  color: 'Blanca', stock: 15 },
      { id: 'sig-bl-m',  sku: 'SIG-BL-M',  size: 'M',  color: 'Blanca', stock: 12 },
      { id: 'sig-bl-l',  sku: 'SIG-BL-L',  size: 'L',  color: 'Blanca', stock: 8  },
      { id: 'sig-bl-xl', sku: 'SIG-BL-XL', size: 'XL', color: 'Blanca', stock: 4  },
    ],
  },
  {
    id: 'sig-negra',
    name: 'Signature Shirt',
    line: 'Signature',
    style: 'Classic',
    priceUSD: 205,
    description: 'The everyday formal. Crisp cotton poplin with a refined spread collar. Effortlessly pristine.',
    images: [
      { id: 'sig-ne-img1', url: '/images/Products/signature-lifestyle.jpg', alt: 'Signature — Negra', isPrimary: true },
    ],
    variants: [
      { id: 'sig-ne-s',  sku: 'SIG-NE-S',  size: 'S',  color: 'Negra', stock: 10 },
      { id: 'sig-ne-m',  sku: 'SIG-NE-M',  size: 'M',  color: 'Negra', stock: 8  },
      { id: 'sig-ne-l',  sku: 'SIG-NE-L',  size: 'L',  color: 'Negra', stock: 4  },
      { id: 'sig-ne-xl', sku: 'SIG-NE-XL', size: 'XL', color: 'Negra', stock: 2  },
    ],
  },

  // ── Essential ─────────────────────────────────────────────────────────────
  {
    id: 'ess-azul-essential',
    name: 'Essential Tee',
    line: 'Essential',
    style: 'Classic',
    priceUSD: 95,
    description: 'The everyday foundation. Supima cotton, relaxed silhouette. Understated by design.',
    images: [
      { id: 'ess-az-img1', url: '/images/Products/essential-blue-tees.jpg',   alt: 'Essential Tee — Azul',    isPrimary: true  },
      { id: 'ess-az-img2', url: '/images/Products/essential-blue-detail.jpg', alt: 'Essential Tee — detalle', isPrimary: false },
    ],
    variants: [
      { id: 'ess-az-s',  sku: 'ESS-AZ-S',  size: 'S',  color: 'Azul Essential', stock: 18 },
      { id: 'ess-az-m',  sku: 'ESS-AZ-M',  size: 'M',  color: 'Azul Essential', stock: 14 },
      { id: 'ess-az-l',  sku: 'ESS-AZ-L',  size: 'L',  color: 'Azul Essential', stock: 10 },
      { id: 'ess-az-xl', sku: 'ESS-AZ-XL', size: 'XL', color: 'Azul Essential', stock: 6  },
    ],
  },
  {
    id: 'ess-negra',
    name: 'Essential Tee',
    line: 'Essential',
    style: 'Classic',
    priceUSD: 95,
    description: 'The everyday foundation. Supima cotton, relaxed silhouette. Understated by design.',
    images: [
      { id: 'ess-ne-img1', url: '/images/Products/essential-blue-tees.jpg', alt: 'Essential Tee — Negra', isPrimary: true },
    ],
    variants: [
      { id: 'ess-ne-s',  sku: 'ESS-NE-S',  size: 'S',  color: 'Negra', stock: 20 },
      { id: 'ess-ne-m',  sku: 'ESS-NE-M',  size: 'M',  color: 'Negra', stock: 15 },
      { id: 'ess-ne-l',  sku: 'ESS-NE-L',  size: 'L',  color: 'Negra', stock: 10 },
      { id: 'ess-ne-xl', sku: 'ESS-NE-XL', size: 'XL', color: 'Negra', stock: 5  },
    ],
  },
  {
    id: 'ess-blanca',
    name: 'Essential Tee',
    line: 'Essential',
    style: 'Classic',
    priceUSD: 95,
    description: 'The everyday foundation. Supima cotton, relaxed silhouette. Understated by design.',
    images: [
      { id: 'ess-bl-img1', url: '/images/Products/essential-white.jpg', alt: 'Essential Tee — Blanca', isPrimary: true },
    ],
    variants: [
      { id: 'ess-bl-s',  sku: 'ESS-BL-S',  size: 'S',  color: 'Blanca', stock: 20 },
      { id: 'ess-bl-m',  sku: 'ESS-BL-M',  size: 'M',  color: 'Blanca', stock: 16 },
      { id: 'ess-bl-l',  sku: 'ESS-BL-L',  size: 'L',  color: 'Blanca', stock: 12 },
      { id: 'ess-bl-xl', sku: 'ESS-BL-XL', size: 'XL', color: 'Blanca', stock: 7  },
    ],
  },
]
