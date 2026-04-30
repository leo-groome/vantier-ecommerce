import { apiClient } from '@/shared/api/client'
import type { HeroSlide, Collection } from '@/features/home/api'

export type { HeroSlide, Collection }

// ── Hero Slides ───────────────────────────────────────────────────────────────

export async function adminListHeroSlides(): Promise<HeroSlide[]> {
  const { data } = await apiClient.get<HeroSlide[]>('/homepage/admin/hero-slides')
  return data
}

export async function adminCreateHeroSlide(payload: {
  label: string
  title: string
  subtitle?: string
  cta_text: string
  cta_url: string
  theme: 'dark' | 'light'
  position: number
  is_active: boolean
}): Promise<HeroSlide> {
  const { data } = await apiClient.post<HeroSlide>('/homepage/admin/hero-slides', payload)
  return data
}

export async function adminUpdateHeroSlide(id: string, payload: Partial<{
  label: string
  title: string
  subtitle: string | null
  cta_text: string
  cta_url: string
  theme: 'dark' | 'light'
  position: number
  is_active: boolean
}>): Promise<HeroSlide> {
  const { data } = await apiClient.patch<HeroSlide>(`/homepage/admin/hero-slides/${id}`, payload)
  return data
}

export async function adminDeleteHeroSlide(id: string): Promise<void> {
  await apiClient.delete(`/homepage/admin/hero-slides/${id}`)
}

export async function adminUploadHeroSlideImage(id: string, file: File): Promise<HeroSlide> {
  const form = new FormData()
  form.append('file', file)
  const { data } = await apiClient.post<HeroSlide>(`/homepage/admin/hero-slides/${id}/image`, form)
  return data
}

// ── Collections ───────────────────────────────────────────────────────────────

export async function adminListCollections(): Promise<Collection[]> {
  const { data } = await apiClient.get<Collection[]>('/homepage/admin/collections')
  return data
}

export async function adminCreateCollection(payload: {
  name: string
  tagline?: string
  label?: string
  price_from?: string
  link_url: string
  position: number
  is_active: boolean
}): Promise<Collection> {
  const { data } = await apiClient.post<Collection>('/homepage/admin/collections', payload)
  return data
}

export async function adminUpdateCollection(id: string, payload: Partial<{
  name: string
  tagline: string | null
  label: string | null
  price_from: string | null
  link_url: string
  position: number
  is_active: boolean
}>): Promise<Collection> {
  const { data } = await apiClient.patch<Collection>(`/homepage/admin/collections/${id}`, payload)
  return data
}

export async function adminDeleteCollection(id: string): Promise<void> {
  await apiClient.delete(`/homepage/admin/collections/${id}`)
}

export async function adminUploadCollectionImage(id: string, file: File): Promise<Collection> {
  const form = new FormData()
  form.append('file', file)
  const { data } = await apiClient.post<Collection>(`/homepage/admin/collections/${id}/image`, form)
  return data
}
