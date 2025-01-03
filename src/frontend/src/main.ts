import { createApp } from 'vue'
import './style.css'
import './assets/index.css'
import App from './App.vue'
import { loader } from '@guolao/vue-monaco-editor'
loader.config({
  paths: {
    vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.43.0/min/vs',
  },
})
createApp(App).mount('#app')
