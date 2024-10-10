import { createRouter, createWebHistory } from 'vue-router'
import WeatherApp from '@/components/WeatherApp.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: WeatherApp
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router