<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  adminListHeroSlides,
  adminCreateHeroSlide,
  adminUpdateHeroSlide,
  adminDeleteHeroSlide,
  adminUploadHeroSlideImage,
  type HeroSlide,
} from '../api'

const slides = ref<HeroSlide[]>([])
const loading = ref(false)
const saving = ref(false)
const error = ref<string | null>(null)

// Modal state
const showModal = ref(false)
const editing = ref<HeroSlide | null>(null)
const form = ref({
  label: '',
  title: '',
  subtitle: '',
  cta_text: 'Explore the Collection',
  cta_url: '/shop',
  theme: 'dark' as 'dark' | 'light',
  position: 0,
  is_active: true,
})

async function load() {
  loading.value = true
  error.value = null
  try {
    slides.value = await adminListHeroSlides()
  } catch (e: any) {
    error.value = e?.response?.data?.detail ?? 'Error al cargar slides'
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editing.value = null
  form.value = {
    label: '',
    title: '',
    subtitle: '',
    cta_text: 'Explore the Collection',
    cta_url: '/shop',
    theme: 'dark',
    position: slides.value.length,
    is_active: true,
  }
  showModal.value = true
}

function openEdit(slide: HeroSlide) {
  editing.value = slide
  form.value = {
    label: slide.label,
    title: slide.title,
    subtitle: slide.subtitle ?? '',
    cta_text: slide.cta_text,
    cta_url: slide.cta_url,
    theme: slide.theme,
    position: slide.position,
    is_active: slide.is_active,
  }
  showModal.value = true
}

async function save() {
  saving.value = true
  error.value = null
  try {
    const payload = {
      ...form.value,
      subtitle: form.value.subtitle || undefined,
    }
    if (editing.value) {
      const updated = await adminUpdateHeroSlide(editing.value.id, payload)
      const idx = slides.value.findIndex(s => s.id === updated.id)
      if (idx !== -1) slides.value[idx] = updated
    } else {
      const created = await adminCreateHeroSlide(payload)
      slides.value.push(created)
    }
    showModal.value = false
  } catch (e: any) {
    error.value = e?.response?.data?.detail ?? 'Error al guardar'
  } finally {
    saving.value = false
  }
}

async function remove(slide: HeroSlide) {
  if (!confirm(`¿Eliminar slide "${slide.title}"?`)) return
  try {
    await adminDeleteHeroSlide(slide.id)
    slides.value = slides.value.filter(s => s.id !== slide.id)
  } catch (e: any) {
    error.value = e?.response?.data?.detail ?? 'Error al eliminar'
  }
}

async function toggleActive(slide: HeroSlide) {
  try {
    const updated = await adminUpdateHeroSlide(slide.id, { is_active: !slide.is_active })
    const idx = slides.value.findIndex(s => s.id === updated.id)
    if (idx !== -1) slides.value[idx] = updated
  } catch (e: any) {
    error.value = e?.response?.data?.detail ?? 'Error'
  }
}

const uploadingId = ref<string | null>(null)
async function handleImageUpload(slide: HeroSlide, event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return
  uploadingId.value = slide.id
  try {
    const updated = await adminUploadHeroSlideImage(slide.id, file)
    const idx = slides.value.findIndex(s => s.id === updated.id)
    if (idx !== -1) slides.value[idx] = updated
  } catch (e: any) {
    error.value = e?.response?.data?.detail ?? 'Error al subir imagen'
  } finally {
    uploadingId.value = null
  }
}

onMounted(load)
</script>

<template>
  <div class="space-y-4">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-[0.9rem] font-bold" style="color: var(--admin-text-primary);">Hero Slides</h2>
        <p class="text-[0.7rem] mt-0.5" style="color: var(--admin-text-secondary);">Imágenes y texto del carrusel principal</p>
      </div>
      <button
        class="px-4 py-2 rounded-lg text-[0.75rem] font-bold uppercase tracking-wide text-white transition-opacity hover:opacity-80"
        style="background: var(--admin-amber);"
        @click="openCreate"
      >+ Nuevo Slide</button>
    </div>

    <!-- Error -->
    <div v-if="error" class="px-4 py-3 rounded-lg text-[0.75rem] text-red-700 bg-red-50 border border-red-200">{{ error }}</div>

    <!-- Loading -->
    <div v-if="loading" class="py-12 text-center text-[0.75rem]" style="color: var(--admin-text-secondary);">Cargando...</div>

    <!-- Empty -->
    <div v-else-if="!slides.length" class="py-12 text-center text-[0.75rem]" style="color: var(--admin-text-secondary);">
      Sin slides. Crea el primero.
    </div>

    <!-- Slides list -->
    <div v-else class="space-y-3">
      <div
        v-for="slide in slides"
        :key="slide.id"
        class="flex gap-4 items-center bg-white rounded-xl p-4 border"
        style="border-color: rgba(0,0,0,0.06);"
      >
        <!-- Thumbnail -->
        <div class="w-20 h-14 rounded-lg overflow-hidden flex-shrink-0 bg-black/5 flex items-center justify-center">
          <img v-if="slide.image_url" :src="slide.image_url" :alt="slide.title" class="w-full h-full object-cover" />
          <span v-else class="text-[0.6rem]" style="color: var(--admin-text-secondary);">Sin imagen</span>
        </div>

        <!-- Info -->
        <div class="flex-1 min-w-0">
          <p class="text-[0.8rem] font-bold truncate" style="color: var(--admin-text-primary);">{{ slide.title }}</p>
          <p class="text-[0.68rem] truncate" style="color: var(--admin-text-secondary);">{{ slide.label }}</p>
          <div class="flex items-center gap-2 mt-1">
            <span
              class="text-[0.6rem] font-bold uppercase px-2 py-0.5 rounded-full"
              :style="slide.theme === 'dark'
                ? { background: '#1a1a1a', color: '#fff' }
                : { background: '#f5f5f0', color: '#333' }"
            >{{ slide.theme }}</span>
            <span class="text-[0.6rem]" style="color: var(--admin-text-secondary);">pos. {{ slide.position }}</span>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center gap-2 flex-shrink-0">
          <!-- Upload image -->
          <label class="cursor-pointer px-3 py-1.5 rounded-lg text-[0.7rem] font-semibold border transition-colors hover:bg-black/[0.03]" style="color: var(--admin-text-secondary); border-color: rgba(0,0,0,0.1);">
            <span v-if="uploadingId === slide.id">Subiendo...</span>
            <span v-else>Imagen</span>
            <input type="file" accept="image/*" class="hidden" :disabled="uploadingId === slide.id" @change="handleImageUpload(slide, $event)" />
          </label>

          <!-- Toggle active -->
          <button
            class="px-3 py-1.5 rounded-lg text-[0.7rem] font-semibold border transition-colors"
            :style="slide.is_active
              ? { color: '#16a34a', borderColor: '#86efac', background: '#f0fdf4' }
              : { color: 'var(--admin-text-secondary)', borderColor: 'rgba(0,0,0,0.1)', background: 'transparent' }"
            @click="toggleActive(slide)"
          >{{ slide.is_active ? 'Activo' : 'Inactivo' }}</button>

          <!-- Edit -->
          <button
            class="px-3 py-1.5 rounded-lg text-[0.7rem] font-semibold border transition-colors hover:bg-black/[0.03]"
            style="color: var(--admin-text-primary); border-color: rgba(0,0,0,0.1);"
            @click="openEdit(slide)"
          >Editar</button>

          <!-- Delete -->
          <button
            class="px-3 py-1.5 rounded-lg text-[0.7rem] font-semibold border border-red-200 text-red-600 hover:bg-red-50 transition-colors"
            @click="remove(slide)"
          >Eliminar</button>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <Teleport to="body">
      <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4" style="background: rgba(0,0,0,0.4);">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg p-6 space-y-4">
          <h3 class="text-[0.9rem] font-bold" style="color: var(--admin-text-primary);">
            {{ editing ? 'Editar Slide' : 'Nuevo Slide' }}
          </h3>

          <div v-if="error" class="px-3 py-2 rounded-lg text-[0.72rem] text-red-700 bg-red-50">{{ error }}</div>

          <div class="grid grid-cols-2 gap-3">
            <div class="col-span-2">
              <label class="block text-[0.68rem] font-bold uppercase tracking-wide mb-1" style="color: var(--admin-text-secondary);">Label / Colección</label>
              <input v-model="form.label" type="text" placeholder="Archival I — Selection 2025" class="w-full px-3 py-2 rounded-lg border text-[0.8rem]" style="border-color: rgba(0,0,0,0.12);" />
            </div>

            <div class="col-span-2">
              <label class="block text-[0.68rem] font-bold uppercase tracking-wide mb-1" style="color: var(--admin-text-secondary);">Título (heading)</label>
              <input v-model="form.title" type="text" placeholder="SILENT EVOLUTION." class="w-full px-3 py-2 rounded-lg border text-[0.8rem]" style="border-color: rgba(0,0,0,0.12);" />
            </div>

            <div class="col-span-2">
              <label class="block text-[0.68rem] font-bold uppercase tracking-wide mb-1" style="color: var(--admin-text-secondary);">Subtítulo (opcional)</label>
              <input v-model="form.subtitle" type="text" placeholder="Timeless Legacy" class="w-full px-3 py-2 rounded-lg border text-[0.8rem]" style="border-color: rgba(0,0,0,0.12);" />
            </div>

            <div>
              <label class="block text-[0.68rem] font-bold uppercase tracking-wide mb-1" style="color: var(--admin-text-secondary);">CTA Text</label>
              <input v-model="form.cta_text" type="text" class="w-full px-3 py-2 rounded-lg border text-[0.8rem]" style="border-color: rgba(0,0,0,0.12);" />
            </div>

            <div>
              <label class="block text-[0.68rem] font-bold uppercase tracking-wide mb-1" style="color: var(--admin-text-secondary);">CTA URL</label>
              <input v-model="form.cta_url" type="text" class="w-full px-3 py-2 rounded-lg border text-[0.8rem]" style="border-color: rgba(0,0,0,0.12);" />
            </div>

            <div>
              <label class="block text-[0.68rem] font-bold uppercase tracking-wide mb-1" style="color: var(--admin-text-secondary);">Tema</label>
              <select v-model="form.theme" class="w-full px-3 py-2 rounded-lg border text-[0.8rem]" style="border-color: rgba(0,0,0,0.12);">
                <option value="dark">Dark</option>
                <option value="light">Light</option>
              </select>
            </div>

            <div>
              <label class="block text-[0.68rem] font-bold uppercase tracking-wide mb-1" style="color: var(--admin-text-secondary);">Posición</label>
              <input v-model.number="form.position" type="number" min="0" class="w-full px-3 py-2 rounded-lg border text-[0.8rem]" style="border-color: rgba(0,0,0,0.12);" />
            </div>

            <div class="col-span-2 flex items-center gap-2">
              <input id="slide-active" v-model="form.is_active" type="checkbox" class="rounded" />
              <label for="slide-active" class="text-[0.78rem]" style="color: var(--admin-text-primary);">Activo (visible en la tienda)</label>
            </div>
          </div>

          <div class="flex justify-end gap-3 pt-2">
            <button class="px-4 py-2 rounded-lg text-[0.75rem] font-semibold border hover:bg-black/[0.03] transition-colors" style="border-color: rgba(0,0,0,0.1); color: var(--admin-text-secondary);" @click="showModal = false">Cancelar</button>
            <button
              class="px-4 py-2 rounded-lg text-[0.75rem] font-bold text-white transition-opacity hover:opacity-80 disabled:opacity-50"
              style="background: var(--admin-amber);"
              :disabled="saving || !form.label || !form.title"
              @click="save"
            >{{ saving ? 'Guardando...' : 'Guardar' }}</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
