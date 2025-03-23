// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'swiper/swiper-bundle.css'
import './assets/main.css' // plik z Tailwind

const app = createApp(App)
app.use(router)
app.mount('#app')
