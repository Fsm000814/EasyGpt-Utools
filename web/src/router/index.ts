import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import MessageChat from '../views/message-chat.vue'
import Translate from '../views/translate.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'message-chat',
    component: MessageChat,
  },
  {
    path: '/translate',
    name: 'translate',
    component: Translate,
  }
]
const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
