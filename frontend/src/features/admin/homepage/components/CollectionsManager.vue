<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  adminListCollections,
  adminCreateCollection,
  adminUpdateCollection,
  adminDeleteCollection,
  adminUploadCollectionImage,
  type Collection,
} from '../api'

const collections = ref<Collection[]>([])
const loading = ref(false)
const saving = ref(false)
const error = ref<string | null>(null)

const showModal = ref(false)
const editing = ref<Collection | null>(null)
const form = ref({
  name: '',
  tagline: '',
  label: '',
  price_from: '',
  link_url: '/shop',
  position: 0,
  is_active: true,
})

async function load() {
  loading.value = true
  error.value = null
  try {
    collections.value = await adminListCollections()
  } catch (e: any) {
    error.value = e?.response?.data?.detail ?? 'Error al cargar colecciones'
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editing.value = null
  form.value = {
    name: '',
    tagline: '',
    label: '',
    price_from: '',
    link_url: '/shop',
    position: collections.value.length,
    is_active: true,
  }
  showModal.value = true
}

function openEdit(col: Collection) {
  editing.value = col
  form.value = {
    name: col.name,
    tagline: col.tagline ?? '',
    label: col.label ?? '',
    price_from: col.price_from ?? '',
    link_url: col.link_url,
    position: col.position,
    is_active: col.is_active,
  }
  showModal.value = true
}

async function save() {
  saving.value = true
  error.value = null
  try {
    const payload = {
      name: form.value.name,
      tagline: form.value.tagline || undefined,
      label: form.value.label || undefined,
      price_from: form.value.price_from || undefined,
      link_url: form.value.link_url,
      position: form.value.position,
      is_active: form.value.is_active,
    }
    if (editing.value) {
      const updated = await adminUpdateCollection(editing.value.id, payload)
      const idx = collections.value.findIndex(c => c.id === updated.id)
      if (idx !== -1) collections.value[idx] = updated
    } else {
      const created = await adminCreateCollection(payload)
      collections.value.push(created)
    }
    showModal.value = false
  } catch (e: any) {
    error.value = e?.response?.data?.detail ?? 'Error al guardar'
  } finally {
    saving.value = false
  }
}

async function remove(col: Collection) {
  if (!confirm(`¿Eliminar colección "${col.name}"?`)) return
  try {
    await adminDeleteCollection(col.id)
    collections.value = collections.value.filter(c => c.id !== col.id)
  } catch (e: any) {
    error.value = e?.response?.data?.detail ?? 'Error al eliminar'
  }
}

async function toggleActive(col: Collection) {
  try {
    const updated = await adminUpdateCollection(col.id, { is_active: !col.is_active })
    const idx = collections.value.findIndex(c => c.id === updated.id)
    if (idx !== -1) collections.value[idx] = updated
  } catch (e: any) {
    error.value = e?.response?.data?.detail ?? 'Error'
  }
}

const uploadingId = ref<string | null>(null)
async function handleImageUpload(col: Collection, event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return
  uploadingId.value = col.id
  try {
    const updated = await adminUploadCollectionImage(col.id, file)
    const idx = collections.value.findIndex(c => c.id === updated.id)
    if (idx !== -1) collections.value[idx] = updated
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
        <h2 class="text-[0.9rem] font-bold" style="color: var(--admin-text-primary);">Colecciones</h2>
        <p class="text-[0.7rem] mt-0.5" style="color: var(--admin-text-secondary);">Tarjetas de líneas de producto en el home</p>
      </div>
      <button
        class="px-4 py-2 rounded-lg text-[0.75rem] font-bold uppercase tracking-wide text-white transition-opacity hover:opacity-80"
        style="background: var(--admin-amber);"
        @click="openCreate"
      >+ Nueva Colección</button>
    </div>

    <!-- Error -->
    <div v-if="error" class="px-4 py-3 rounded-lg text-[0.75rem] text-red-700 bg-red-50 border border-red-200">{{ error }}</div>

    <!-- Loading -->
    <div v-if="loading" class="py-12 text-center text-[0.75rem]" style="color: var(--admin-text-secondary);">Cargando...</div>

    <!-- Empty -->
    <div v-else-if="!collections.length" class="py-12 text-center text-[0.75rem]" style="color: var(--admin-text-secondary);">
      Sin colecciones. Crea la primera.
    </div>

    <!-- Collections list -->
    <div v-else class="space-y-3">
      <div
        v-for="col in collections"
        :key="col.id"
        class="flex gap-4 items-center bg-white rounded-xl p-4 border"
        style="border-color: rgba(0,0,0,0.06);"
      >
        <!-- Thumbnail -->
        <div class="w-20 h-14 rounded-lg overflow-hidden flex-shrink-0 bg-black/5 flex items-center justify-center">
          <img v-if="col.image_url" :src="col.image_url" :alt="col.name" class="w-full h-full object-cover" />
          <span v-else class="text-[0.6rem]" style="color: var(--admin-text-secondary);">Sin imagen</span>
        </div>

        <!-- Info -->
        <div class="flex-1 min-w-0">
          <p class="text-[0.8rem] font-bold truncate" style="color: var(--admin-text-primary);">{{ col.name }}</p>
          <p class="text-[0.68rem] truncate" style="color: var(--admin-text-secondary);">{{ col.tagline }}</p>
          <div class="flex items-center gap-3 mt-1">
            <span v-if="col.label" class="text-[0.6rem]" style="color: var(--admin-text-secondary);">{{ col.label }}</span>
            <span v-if="col.price_from" class="text-[0.6rem] font-semibold" style="color: var(--admin-amber);">{{ col.price_from }}</span>
            <span class="text-[0.6rem]" style="color: var(--admin-text-secondary);">pos. {{ col.position }}</span>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center gap-2 flex-shrink-0">
          <!-- Upload image -->
          <label class="cursor-pointer px-3 py-1.5 rounded-lg text-[0.7rem] font-semibold border transition-colors hover:bg-black/[0.03]" style="color: var(--admin-text-secondary); border-color: rgba(0,0,0,0.1);">
            <span v-if="uploadingId === col.id">Subiendo...</span>
            <span v-else>Imagen</span>
            <input type="file" accept="image/*" class="hidden" :disabled="uploadingId === col.id" @change="handleImageUpload(col, $event)" />
          </label>

          <!-- Toggle active -->
          <button
            class="px-3 py-1.5 rounded-lg text-[0.7rem] font-semibold border transition-colors"
            :style="col.is_active
              ? { color: '#16a34a', borderColor: '#86efac', background: '#f0fdf4' }
              : { color: 'var(--admin-text-secondary)', borderColor: 'rgba(0,0,0,0.1)', background: 'transparent' }"
            @click="toggleActive(col)"
          >{{ col.is_active ? 'Activo' : 'Inactivo' }}</button>

          <!-- Edit -->
          <button
            class="px-3 py-1.5 rounded-lg text-[0.7rem] font-semibold border transition-colors hover:bg-black/[0.03]"
            style="color: var(--admin-text-primary); border-color: rgba(0,0,0,0.1);"
            @click="openEdit(col)"
          >Editar</button>

          <!-- Delete -->
          <button
            class="px-3 py-1.5 rounded-lg text-[0.7rem] font-semibold border border-red-200 text-red-600 hover:bg-red-50 transition-colors"
            @click="remove(col)"
          >Eliminar</button>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <Teleport to="body">
      <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4" style="background: rgba(0,0,0,0.4);">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg p-6 space-y-4">
          <h3 class="text-[0.9rem] font-bold" style="color: var(--admin-text-primary);">
            {{ editing ? 'Editar Colección' : 'Nueva Colección' }}
          </h3>

          <div v-if="error" class="px-3 py-2 rounded-lg text-[0.72rem] text-red-700 bg-red-50">{{ error }}</div>

          <div class="grid grid-cols-2 gap-3">
            <div class="col-span-2">
              <label class="block text-[0.68rem] font-bold uppercase tracking-wide mb-1" style="color: var(--admin-text-secondary);">Nombre *</label>
              <input v-model="form.name" type="text" placeholder="Polo Atelier" class="w-full px-3 py-2 rounded-lg border text-[0.8rem]" style="border-color: rgba(0,0,0,0.12);" />
            </div>

            <div class="col-span-2">
              <label class="block text-[0.68rem] font-bold uppercase tracking-wide mb-1" style="color: var(--admin-text-secondary);">Tagline</label>
              <input v-model="form.tagline" type="text" placeholder="Structural excellence" class="w-full px-3 py-2 rounded-lg border text-[0.8rem]" style="border-color: rgba(0,0,0,0.12);" />
            </div>

            <div>
              <label class="block text-[0.68rem] font-bold uppercase tracking-wide mb-1" style="color: var(--admin-text-secondary);">Label (ej. Outerwear)</label>
              <input v-model="form.label" type="text" class="w-full px-3 py-2 rounded-lg border text-[0.8rem]" style="border-color: rgba(0,0,0,0.12);" />
            </div>

            <div>
              <label class="block text-[0.68rem] font-bold uppercase tracking-wide mb-1" style="color: var(--admin-text-secondary);">Precio desde (ej. From $180)</label>
              <input v-model="form.price_from" type="text" class="w-full px-3 py-2 rounded-lg border text-[0.8rem]" style="border-color: rgba(0,0,0,0.12);" />
            </div>

            <div>
              <label class="block text-[0.68rem] font-bold uppercase tracking-wide mb-1" style="color: var(--admin-text-secondary);">Link URL</label>
              <input v-model="form.link_url" type="text" class="w-full px-3 py-2 rounded-lg border text-[0.8rem]" style="border-color: rgba(0,0,0,0.12);" />
            </div>

            <div>
              <label class="block text-[0.68rem] font-bold uppercase tracking-wide mb-1" style="color: var(--admin-text-secondary);">Posición</label>
              <input v-model.number="form.position" type="number" min="0" class="w-full px-3 py-2 rounded-lg border text-[0.8rem]" style="border-color: rgba(0,0,0,0.12);" />
            </div>

            <div class="col-span-2 flex items-center gap-2">
              <input id="col-active" v-model="form.is_active" type="checkbox" class="rounded" />
              <label for="col-active" class="text-[0.78rem]" style="color: var(--admin-text-primary);">Activo (visible en la tienda)</label>
            </div>
          </div>

          <div class="flex justify-end gap-3 pt-2">
            <button class="px-4 py-2 rounded-lg text-[0.75rem] font-semibold border hover:bg-black/[0.03] transition-colors" style="border-color: rgba(0,0,0,0.1); color: var(--admin-text-secondary);" @click="showModal = false">Cancelar</button>
            <button
              class="px-4 py-2 rounded-lg text-[0.75rem] font-bold text-white transition-opacity hover:opacity-80 disabled:opacity-50"
              style="background: var(--admin-amber);"
              :disabled="saving || !form.name"
              @click="save"
            >{{ saving ? 'Guardando...' : 'Guardar' }}</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
