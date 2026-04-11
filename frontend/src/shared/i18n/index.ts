import { createI18n } from 'vue-i18n'

export const i18n = createI18n({
  legacy: false,
  locale: 'es',
  fallbackLocale: 'en',
  messages: {
    es: {},
    en: {},
  },
})

// Lazy-load a slice's locale messages and merge them
export async function loadSliceMessages(
  slice: string,
  locale: 'es' | 'en'
): Promise<void> {
  try {
    const messages = await import(`../../features/${slice}/i18n/${locale}.json`)
    i18n.global.mergeLocaleMessage(locale, { [slice]: messages.default })
  } catch {
    // Slice has no i18n yet — skip silently
  }
}
