import { apiClient } from '@/shared/api/client'

export interface HeroSlide {
  id: string
  label: string
  title: string
  subtitle: string | null
  cta_text: string
  cta_url: string
  image_url: string | null
  theme: 'dark' | 'light'
  position: number
  is_active: boolean
}

export interface Collection {
  id: string
  name: string
  tagline: string | null
  label: string | null
  price_from: string | null
  link_url: string
  image_url: string | null
  position: number
  is_active: boolean
}

export async function fetchHeroSlides(): Promise<HeroSlide[]> {
  const { data } = await apiClient.get<HeroSlide[]>('/homepage/hero-slides')
  return data
}

export async function fetchCollections(): Promise<Collection[]> {
  const { data } = await apiClient.get<Collection[]>('/homepage/collections')
  return data
}
