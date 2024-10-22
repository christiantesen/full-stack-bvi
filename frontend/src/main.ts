import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './index.css'

import Home from './pages/Home.vue'
import Publications from './pages/Publications.vue'
import Favorites from './pages/Favorites.vue'
import ReadLater from './pages/ReadLater.vue'
import Profile from './pages/Profile.vue'

import { makeServer } from './mocks/server'

if (process.env.NODE_ENV === 'development') {
  makeServer()
}

const routes = [
  { path: '/', component: Home },
  { path: '/publications', component: Publications },
  { path: '/favorites', component: Favorites },
  { path: '/read-later', component: ReadLater },
  { path: '/profile', component: Profile },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

createApp(App).use(router).mount('#app')