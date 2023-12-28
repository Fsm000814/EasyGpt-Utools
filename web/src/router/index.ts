import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import MessageChat from '../views/message-chat/message-chat.vue'
import Translate from '../views/trans-late.vue'
import Setting from '../views/settings/message-setting.vue'
import TemplateConfiguration from '../views/template-configuration/template-configuration.vue'
import { close, start } from '../utils/nprogress';

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
  },
  {
    path: '/message-setting',
    name: 'message-setting',
    component: Setting,
  }
]
const router = createRouter({
  history: createWebHashHistory(),
  routes
})
// 路由前置后卫
router.beforeEach(() => {
	// 开启进度条
	start();
});
// 路由后置后卫
router.afterEach(() => {
	// 关闭进度条
	close();
});
export default router
