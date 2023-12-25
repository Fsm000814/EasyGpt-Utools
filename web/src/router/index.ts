import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import MessageChat from '../views/message-chat/message-chat.vue'
import Translate from '../views/trans-late.vue'
import TemplateConfiguration from '../views/template-configuration/template-configuration.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/message-chat',
    name: 'message-chat',
    component: MessageChat,
  },
  {
    path: '/trans-late',
    name: 'trans-late',
    component: Translate,
  },
  {
    path: '/template-configuration',
    name: 'template-configuration',
    component: TemplateConfiguration,
  }
]
const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
