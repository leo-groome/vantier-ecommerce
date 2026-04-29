import type { Product } from './types'

// ─── Real Vantier color palette ───────────────────────────────────────────────
export const COLOR_BG: Record<string, string> = {
  // ── Vantier branded palette ──────────────────────────────────────────────
  'Azul Vantier':    '#869AEB',
  'Beige Verano':    '#E8E6D6',
  'Naranja Vantier': '#F2955E',
  'Blanca':          '#FFFFFF',
  'Negra':           '#000000',
  'Beige Atelier':   '#C9BFA8',
  'Azul Navy':       '#202646',
  'Azul Essential':  '#2D3FA6',
  // ── Generic English names (backend DB values) ────────────────────────────
  'Black':   '#111111',
  'White':   '#F5F5F0',
  'Blue':    '#2563EB',
  'Orange':  '#EA580C',
  'Beige':   '#D4C5A9',
  'Red':     '#DC2626',
  'Green':   '#16A34A',
  'Gray':    '#9CA3AF',
  'Grey':    '#9CA3AF',
  'Navy':    '#1E3A5F',
  'Purple':  '#7C3AED',
  'Pink':    '#DB2777',
  'Brown':   '#92400E',
  'Yellow':  '#CA8A04',
  'Teal':    '#0D9488',
  'Ivory':   '#F5F0E8',
  'Cream':   '#F0E8D8',
  'Coral':   '#FF6B6B',
  'Charcoal':'#374151',
}

export const COLOR_TEXT: Record<string, string> = {
  // ── Vantier branded palette ──────────────────────────────────────────────
  'Azul Vantier':    '#FFFFFF',
  'Beige Verano':    '#000000',
  'Naranja Vantier': '#FFFFFF',
  'Blanca':          '#000000',
  'Negra':           '#FFFFFF',
  'Beige Atelier':   '#000000',
  'Azul Navy':       '#FFFFFF',
  'Azul Essential':  '#FFFFFF',
  // ── Generic English names ────────────────────────────────────────────────
  'Black': '#FFFFFF', 'White': '#000000', 'Blue': '#FFFFFF',
  'Orange': '#FFFFFF', 'Beige': '#000000', 'Red': '#FFFFFF',
  'Green': '#FFFFFF', 'Navy': '#FFFFFF', 'Purple': '#FFFFFF',
  'Pink': '#FFFFFF', 'Yellow': '#000000', 'Ivory': '#000000',
  'Cream': '#000000', 'Coral': '#FFFFFF', 'Teal': '#FFFFFF',
  'Gray': '#000000', 'Grey': '#000000', 'Charcoal': '#FFFFFF',
}

export const MOCK_PRODUCTS: Product[] = [
  // ── Polo Atelier ──────────────────────────────────────────────────────────
  {
    id: 'pa-classic-beige',
    name: 'Polo Atelier — Classic',
    line: 'polo_atelier',
    description: 'The cornerstone piece. Crafted from 100% Pima cotton with a structured collar and refined silhouette.',
    is_active: true,
    variants: [
      { id: 'pa-cb-s',  sku: 'PA-CL-BEI-S',  style: 'classic', size: 'S',  color: 'Beige Atelier', stock_qty: 12, price_usd: '180.00', is_active: true, images: [{ id: 'img-pa-cb-1', url: '/images/Products/polo-atelier-beige-folded.jpg', alt_text: 'Beige Atelier Folded', position: 1 }] },
      { id: 'pa-cb-m',  sku: 'PA-CL-BEI-M',  style: 'classic', size: 'M',  color: 'Beige Atelier', stock_qty: 8,  price_usd: '180.00', is_active: true, images: [{ id: 'img-pa-cb-2', url: '/images/Products/polo-atelier-beige-folded.jpg', alt_text: 'Beige Atelier Folded', position: 1 }] },
      { id: 'pa-cb-l',  sku: 'PA-CL-BEI-L',  style: 'classic', size: 'L',  color: 'Beige Atelier', stock_qty: 3,  price_usd: '180.00', is_active: true, images: [{ id: 'img-pa-cb-3', url: '/images/Products/polo-atelier-beige-folded.jpg', alt_text: 'Beige Atelier Folded', position: 1 }] },
      { id: 'pa-cb-xl', sku: 'PA-CL-BEI-XL', style: 'classic', size: 'XL', color: 'Beige Atelier', stock_qty: 6,  price_usd: '180.00', is_active: true, images: [{ id: 'img-pa-cb-4', url: '/images/Products/polo-atelier-beige-folded.jpg', alt_text: 'Beige Atelier Folded', position: 1 }] },
    ],
  },
  {
    id: 'pa-classic-navy',
    name: 'Polo Atelier — Classic',
    line: 'polo_atelier',
    description: 'The cornerstone piece. Crafted from 100% Pima cotton with a structured collar and refined silhouette.',
    is_active: true,
    variants: [
      { id: 'pa-cn-s',  sku: 'PA-CL-NAV-S',  style: 'classic', size: 'S',  color: 'Azul Navy', stock_qty: 10, price_usd: '180.00', is_active: true, images: [{ id: 'img-pa-cn-1', url: '/images/Products/polo-atelier-jackets-stacked.jpg', alt_text: 'Azul Navy Stacked', position: 1 }] },
      { id: 'pa-cn-m',  sku: 'PA-CL-NAV-M',  style: 'classic', size: 'M',  color: 'Azul Navy', stock_qty: 6,  price_usd: '180.00', is_active: true, images: [{ id: 'img-pa-cn-2', url: '/images/Products/polo-atelier-jackets-stacked.jpg', alt_text: 'Azul Navy Stacked', position: 1 }] },
      { id: 'pa-cn-l',  sku: 'PA-CL-NAV-L',  style: 'classic', size: 'L',  color: 'Azul Navy', stock_qty: 0,  price_usd: '180.00', is_active: true, images: [{ id: 'img-pa-cn-3', url: '/images/Products/polo-atelier-jackets-stacked.jpg', alt_text: 'Azul Navy Stacked', position: 1 }] },
      { id: 'pa-cn-xl', sku: 'PA-CL-NAV-XL', style: 'classic', size: 'XL', color: 'Azul Navy', stock_qty: 4,  price_usd: '180.00', is_active: true, images: [{ id: 'img-pa-cn-4', url: '/images/Products/polo-atelier-jackets-stacked.jpg', alt_text: 'Azul Navy Stacked', position: 1 }] },
    ],
  },
  {
    id: 'pa-classic-negra',
    name: 'Polo Atelier — Classic',
    line: 'polo_atelier',
    description: 'The cornerstone piece. Crafted from 100% Pima cotton with a structured collar and refined silhouette.',
    is_active: true,
    variants: [
      { id: 'pa-co-s',  sku: 'PA-CL-NEG-S',  style: 'classic', size: 'S',  color: 'Negra', stock_qty: 9,  price_usd: '180.00', is_active: true, images: [{ id: 'img-pa-neg-1', url: '/images/Products/polo-atelier-jackets-stacked.jpg', alt_text: 'Negra Stacked', position: 1 }] },
      { id: 'pa-co-m',  sku: 'PA-CL-NEG-M',  style: 'classic', size: 'M',  color: 'Negra', stock_qty: 7,  price_usd: '180.00', is_active: true, images: [{ id: 'img-pa-neg-2', url: '/images/Products/polo-atelier-jackets-stacked.jpg', alt_text: 'Negra Stacked', position: 1 }] },
      { id: 'pa-co-l',  sku: 'PA-CL-NEG-L',  style: 'classic', size: 'L',  color: 'Negra', stock_qty: 3,  price_usd: '180.00', is_active: true, images: [{ id: 'img-pa-neg-3', url: '/images/Products/polo-atelier-jackets-stacked.jpg', alt_text: 'Negra Stacked', position: 1 }] },
      { id: 'pa-co-xl', sku: 'PA-CL-NEG-XL', style: 'classic', size: 'XL', color: 'Negra', stock_qty: 5,  price_usd: '180.00', is_active: true, images: [{ id: 'img-pa-neg-4', url: '/images/Products/polo-atelier-jackets-stacked.jpg', alt_text: 'Negra Stacked', position: 1 }] },
    ],
  },

  // ── Signature ─────────────────────────────────────────────────────────────
  {
    id: 'sig-azul-vantier',
    name: 'Signature Shirt',
    line: 'signature',
    description: 'Impeccably tailored. Woven from premium long-staple Egyptian cotton for a drape that commands presence.',
    is_active: true,
    variants: [
      { id: 'sig-az-s',  sku: 'SIG-AZ-S',  style: 'design', size: 'S',  color: 'Azul Vantier', stock_qty: 8, price_usd: '220.00', is_active: true, images: [{ id: 'img-sig-az-1', url: '/images/Products/signature-lifestyle.jpg', alt_text: 'Signature Azul Vantier', position: 1 }] },
      { id: 'sig-az-m',  sku: 'SIG-AZ-M',  style: 'design', size: 'M',  color: 'Azul Vantier', stock_qty: 6, price_usd: '220.00', is_active: true, images: [{ id: 'img-sig-az-2', url: '/images/Products/signature-lifestyle.jpg', alt_text: 'Signature Azul Vantier', position: 1 }] },
      { id: 'sig-az-l',  sku: 'SIG-AZ-L',  style: 'design', size: 'L',  color: 'Azul Vantier', stock_qty: 4, price_usd: '220.00', is_active: true, images: [{ id: 'img-sig-az-3', url: '/images/Products/signature-lifestyle.jpg', alt_text: 'Signature Azul Vantier', position: 1 }] },
      { id: 'sig-az-xl', sku: 'SIG-AZ-XL', style: 'design', size: 'XL', color: 'Azul Vantier', stock_qty: 2, price_usd: '220.00', is_active: true, images: [{ id: 'img-sig-az-4', url: '/images/Products/signature-lifestyle.jpg', alt_text: 'Signature Azul Vantier', position: 1 }] },
    ],
  },
  {
    id: 'sig-beige-verano',
    name: 'Signature Shirt',
    line: 'signature',
    description: 'The everyday formal. Crisp cotton poplin with a refined spread collar. Effortlessly pristine.',
    is_active: true,
    variants: [
      { id: 'sig-be-s',  sku: 'SIG-BE-S',  style: 'classic', size: 'S',  color: 'Beige Verano', stock_qty: 10, price_usd: '205.00', is_active: true, images: [{ id: 'img-sig-be-1', url: '/images/Products/signature-blazer-street.jpg', alt_text: 'Signature Beige Verano', position: 1 }] },
      { id: 'sig-be-m',  sku: 'SIG-BE-M',  style: 'classic', size: 'M',  color: 'Beige Verano', stock_qty: 8,  price_usd: '205.00', is_active: true, images: [{ id: 'img-sig-be-2', url: '/images/Products/signature-blazer-street.jpg', alt_text: 'Signature Beige Verano', position: 1 }] },
      { id: 'sig-be-l',  sku: 'SIG-BE-L',  style: 'classic', size: 'L',  color: 'Beige Verano', stock_qty: 5,  price_usd: '205.00', is_active: true, images: [{ id: 'img-sig-be-3', url: '/images/Products/signature-blazer-street.jpg', alt_text: 'Signature Beige Verano', position: 1 }] },
    ],
  },
  {
    id: 'sig-naranja-vantier',
    name: 'Signature Shirt',
    line: 'signature',
    description: 'Arquitectura de color. Una declaración de presencia sin esfuerzo en algodón egipcio de primera calidad.',
    is_active: true,
    variants: [
      { id: 'sig-na-s',  sku: 'SIG-NA-S',  style: 'design', size: 'S',  color: 'Naranja Vantier', stock_qty: 6, price_usd: '220.00', is_active: true, images: [{ id: 'img-sig-na-1', url: '/images/Products/signature-lifestyle.jpg', alt_text: 'Signature Naranja Vantier', position: 1 }] },
      { id: 'sig-na-m',  sku: 'SIG-NA-M',  style: 'design', size: 'M',  color: 'Naranja Vantier', stock_qty: 5, price_usd: '220.00', is_active: true, images: [{ id: 'img-sig-na-2', url: '/images/Products/signature-lifestyle.jpg', alt_text: 'Signature Naranja Vantier', position: 1 }] },
      { id: 'sig-na-l',  sku: 'SIG-NA-L',  style: 'design', size: 'L',  color: 'Naranja Vantier', stock_qty: 3, price_usd: '220.00', is_active: true, images: [{ id: 'img-sig-na-3', url: '/images/Products/signature-lifestyle.jpg', alt_text: 'Signature Naranja Vantier', position: 1 }] },
    ],
  },
  {
    id: 'sig-blanca',
    name: 'Signature Shirt',
    line: 'signature',
    description: 'The everyday formal. Crisp cotton poplin with a refined spread collar. Effortlessly pristine.',
    is_active: true,
    variants: [
      { id: 'sig-bl-s',  sku: 'SIG-BL-S',  style: 'classic', size: 'S',  color: 'Blanca', stock_qty: 15, price_usd: '205.00', is_active: true, images: [{ id: 'img-sig-bl-1', url: '/images/Products/signature-blazer-street.jpg', alt_text: 'Signature Blanca', position: 1 }] },
      { id: 'sig-bl-m',  sku: 'SIG-BL-M',  style: 'classic', size: 'M',  color: 'Blanca', stock_qty: 12, price_usd: '205.00', is_active: true, images: [{ id: 'img-sig-bl-2', url: '/images/Products/signature-blazer-street.jpg', alt_text: 'Signature Blanca', position: 1 }] },
      { id: 'sig-bl-l',  sku: 'SIG-BL-L',  style: 'classic', size: 'L',  color: 'Blanca', stock_qty: 8,  price_usd: '205.00', is_active: true, images: [{ id: 'img-sig-bl-3', url: '/images/Products/signature-blazer-street.jpg', alt_text: 'Signature Blanca', position: 1 }] },
      { id: 'sig-bl-xl', sku: 'SIG-BL-XL', style: 'classic', size: 'XL', color: 'Blanca', stock_qty: 4,  price_usd: '205.00', is_active: true, images: [{ id: 'img-sig-bl-4', url: '/images/Products/signature-blazer-street.jpg', alt_text: 'Signature Blanca', position: 1 }] },
    ],
  },
  {
    id: 'sig-negra',
    name: 'Signature Shirt',
    line: 'signature',
    description: 'The everyday formal. Crisp cotton poplin with a refined spread collar. Effortlessly pristine.',
    is_active: true,
    variants: [
      { id: 'sig-ne-s',  sku: 'SIG-NE-S',  style: 'classic', size: 'S',  color: 'Negra', stock_qty: 10, price_usd: '205.00', is_active: true, images: [{ id: 'img-sig-ne-1', url: '/images/Products/signature-lifestyle.jpg', alt_text: 'Signature Negra', position: 1 }] },
      { id: 'sig-ne-m',  sku: 'SIG-NE-M',  style: 'classic', size: 'M',  color: 'Negra', stock_qty: 8,  price_usd: '205.00', is_active: true, images: [{ id: 'img-sig-ne-2', url: '/images/Products/signature-lifestyle.jpg', alt_text: 'Signature Negra', position: 1 }] },
      { id: 'sig-ne-l',  sku: 'SIG-NE-L',  style: 'classic', size: 'L',  color: 'Negra', stock_qty: 4,  price_usd: '205.00', is_active: true, images: [{ id: 'img-sig-ne-3', url: '/images/Products/signature-lifestyle.jpg', alt_text: 'Signature Negra', position: 1 }] },
      { id: 'sig-ne-xl', sku: 'SIG-NE-XL', style: 'classic', size: 'XL', color: 'Negra', stock_qty: 2,  price_usd: '205.00', is_active: true, images: [{ id: 'img-sig-ne-4', url: '/images/Products/signature-lifestyle.jpg', alt_text: 'Signature Negra', position: 1 }] },
    ],
  },

  // ── Essential ─────────────────────────────────────────────────────────────
  {
    id: 'ess-azul-essential',
    name: 'Essential Tee',
    line: 'essential',
    description: 'The everyday foundation. Supima cotton, relaxed silhouette. Understated by design.',
    is_active: true,
    variants: [
      { id: 'ess-az-s',  sku: 'ESS-AZ-S',  style: 'classic', size: 'S',  color: 'Azul Essential', stock_qty: 18, price_usd: '95.00', is_active: true, images: [{ id: 'img-ess-az-1', url: '/images/Products/essential-blue-tees.jpg', alt_text: 'Essential Tee Azul', position: 1 }] },
      { id: 'ess-az-m',  sku: 'ESS-AZ-M',  style: 'classic', size: 'M',  color: 'Azul Essential', stock_qty: 14, price_usd: '95.00', is_active: true, images: [{ id: 'img-ess-az-2', url: '/images/Products/essential-blue-tees.jpg', alt_text: 'Essential Tee Azul', position: 1 }] },
      { id: 'ess-az-l',  sku: 'ESS-AZ-L',  style: 'classic', size: 'L',  color: 'Azul Essential', stock_qty: 10, price_usd: '95.00', is_active: true, images: [{ id: 'img-ess-az-3', url: '/images/Products/essential-blue-tees.jpg', alt_text: 'Essential Tee Azul', position: 1 }] },
      { id: 'ess-az-xl', sku: 'ESS-AZ-XL', style: 'classic', size: 'XL', color: 'Azul Essential', stock_qty: 6,  price_usd: '95.00', is_active: true, images: [{ id: 'img-ess-az-4', url: '/images/Products/essential-blue-tees.jpg', alt_text: 'Essential Tee Azul', position: 1 }] },
    ],
  },
  {
    id: 'ess-negra',
    name: 'Essential Tee',
    line: 'essential',
    description: 'The everyday foundation. Supima cotton, relaxed silhouette. Understated by design.',
    is_active: true,
    variants: [
      { id: 'ess-ne-s',  sku: 'ESS-NE-S',  style: 'classic', size: 'S',  color: 'Negra', stock_qty: 20, price_usd: '95.00', is_active: true, images: [{ id: 'img-ess-ne-1', url: '/images/Products/essential-blue-tees.jpg', alt_text: 'Essential Tee Negra', position: 1 }] },
      { id: 'ess-ne-m',  sku: 'ESS-NE-M',  style: 'classic', size: 'M',  color: 'Negra', stock_qty: 15, price_usd: '95.00', is_active: true, images: [{ id: 'img-ess-ne-2', url: '/images/Products/essential-blue-tees.jpg', alt_text: 'Essential Tee Negra', position: 1 }] },
      { id: 'ess-ne-l',  sku: 'ESS-NE-L',  style: 'classic', size: 'L',  color: 'Negra', stock_qty: 10, price_usd: '95.00', is_active: true, images: [{ id: 'img-ess-ne-3', url: '/images/Products/essential-blue-tees.jpg', alt_text: 'Essential Tee Negra', position: 1 }] },
      { id: 'ess-ne-xl', sku: 'ESS-NE-XL', style: 'classic', size: 'XL', color: 'Negra', stock_qty: 5,  price_usd: '95.00', is_active: true, images: [{ id: 'img-ess-ne-4', url: '/images/Products/essential-blue-tees.jpg', alt_text: 'Essential Tee Negra', position: 1 }] },
    ],
  },
  {
    id: 'ess-blanca',
    name: 'Essential Tee',
    line: 'essential',
    description: 'The everyday foundation. Supima cotton, relaxed silhouette. Understated by design.',
    is_active: true,
    variants: [
      { id: 'ess-bl-s',  sku: 'ESS-BL-S',  style: 'classic', size: 'S',  color: 'Blanca', stock_qty: 20, price_usd: '95.00', is_active: true, images: [{ id: 'img-ess-bl-1', url: '/images/Products/essential-white.jpg', alt_text: 'Essential Tee Blanca', position: 1 }] },
      { id: 'ess-bl-m',  sku: 'ESS-BL-M',  style: 'classic', size: 'M',  color: 'Blanca', stock_qty: 16, price_usd: '95.00', is_active: true, images: [{ id: 'img-ess-bl-2', url: '/images/Products/essential-white.jpg', alt_text: 'Essential Tee Blanca', position: 1 }] },
      { id: 'ess-bl-l',  sku: 'ESS-BL-L',  style: 'classic', size: 'L',  color: 'Blanca', stock_qty: 12, price_usd: '95.00', is_active: true, images: [{ id: 'img-ess-bl-3', url: '/images/Products/essential-white.jpg', alt_text: 'Essential Tee Blanca', position: 1 }] },
      { id: 'ess-bl-xl', sku: 'ESS-BL-XL', style: 'classic', size: 'XL', color: 'Blanca', stock_qty: 7,  price_usd: '95.00', is_active: true, images: [{ id: 'img-ess-bl-4', url: '/images/Products/essential-white.jpg', alt_text: 'Essential Tee Blanca', position: 1 }] },
    ],
  },
]
