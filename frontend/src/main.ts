import { createApp } from 'vue'
import App from './app/App.vue'
import router from './app/router'
import { pinia } from './app/plugins/pinia'
import { i18n } from './shared/i18n'
import './style.css'

createApp(App)
  .use(pinia)
  .use(router)
  .use(i18n)
  .mount('#app')
