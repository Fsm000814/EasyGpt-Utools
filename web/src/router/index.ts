import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import MainLayout from '../views/main-layout.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'main-layout',
    component: MainLayout
  },
]
const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
