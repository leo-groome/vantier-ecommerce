import { createApp } from 'vue'
import { createHead } from '@vueuse/head'
import App from './app/App.vue'
import router from './app/router'
import { pinia } from './app/plugins/pinia'
import { i18n } from './shared/i18n'
import { useAuthStore } from './features/auth/store'
import './style.css'

const head = createHead()

const app = createApp(App)
  .use(pinia)
  .use(router)
  .use(i18n)
  .use(head)

// Sync Neon Auth session before first router navigation (deferred until mount).
// This ensures guards have accurate auth state on initial deep-link loads.
const auth = useAuthStore()
auth.syncFromNeonAuth().finally(() => app.mount('#app'))
