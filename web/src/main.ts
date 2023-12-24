import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Ant from "ant-design-vue";
import 'ant-design-vue/dist/reset.css';

createApp(App)
    .use(router)
    .use(Ant)
    .mount('#app')
