import { ref } from 'vue'

export type ToastVariant = 'default' | 'success' | 'error'

export interface Toast {
  id: number
  message: string
  variant: ToastVariant
}

const toasts = ref<Toast[]>([])
let nextId = 0

export function useToast() {
  function show(message: string, variant: ToastVariant = 'default', duration = 3000) {
    const id = ++nextId
    toasts.value.push({ id, message, variant })
    setTimeout(() => dismiss(id), duration)
  }

  function dismiss(id: number) {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }

  return { toasts, show, dismiss }
}
