<script lang="ts">
export type AdminStatus =
  | 'ok' | 'bajo' | 'critico'
  | 'activo' | 'inactivo' | 'expirado'
  | 'pendiente' | 'procesando'
  | 'enviado' | 'entregado'
  | 'confirmada' | 'recibida' | 'en_transito'
</script>

<script setup lang="ts">
import type { AdminStatus } from './StatusBadge.vue'

defineProps<{ status: AdminStatus }>()

const LABELS: Record<AdminStatus, string> = {
  ok: 'OK', bajo: 'Bajo', critico: 'Crítico',
  activo: 'Activo', inactivo: 'Inactivo', expirado: 'Expirado',
  pendiente: 'Pendiente', procesando: 'Procesando',
  enviado: 'Enviado', entregado: 'Entregado',
  confirmada: 'Confirmada', recibida: 'Recibida', en_transito: 'En tránsito',
}

const COLORS: Record<AdminStatus, { bg: string; text: string }> = {
  ok:          { bg: 'var(--status-ok-bg)',   text: 'var(--status-ok-text)'   },
  activo:      { bg: 'var(--status-ok-bg)',   text: 'var(--status-ok-text)'   },
  entregado:   { bg: 'var(--status-ok-bg)',   text: 'var(--status-ok-text)'   },
  confirmada:  { bg: 'var(--status-ok-bg)',   text: 'var(--status-ok-text)'   },
  bajo:        { bg: 'var(--status-warn-bg)', text: 'var(--status-warn-text)' },
  procesando:  { bg: 'var(--status-warn-bg)', text: 'var(--status-warn-text)' },
  en_transito: { bg: 'var(--status-warn-bg)', text: 'var(--status-warn-text)' },
  critico:     { bg: 'var(--status-crit-bg)', text: 'var(--status-crit-text)' },
  inactivo:    { bg: 'var(--status-crit-bg)', text: 'var(--status-crit-text)' },
  expirado:    { bg: 'var(--status-crit-bg)', text: 'var(--status-crit-text)' },
  enviado:     { bg: 'var(--status-ship-bg)', text: 'var(--status-ship-text)' },
  recibida:    { bg: 'var(--status-ship-bg)', text: 'var(--status-ship-text)' },
  pendiente:   { bg: 'var(--status-pend-bg)', text: 'var(--status-pend-text)' },
}
</script>

<template>
  <span
    class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full font-medium whitespace-nowrap"
    style="font-size: 0.68rem;"
    :style="{ background: COLORS[status].bg, color: COLORS[status].text }"
  >
    <span
      class="w-1.5 h-1.5 rounded-full flex-shrink-0"
      :style="{ background: COLORS[status].text }"
    />
    {{ LABELS[status] }}
  </span>
</template>
